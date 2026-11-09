"""L'API della cineteca su PostgreSQL: CRUD con SQLAlchemy ORM e una Session aperta dentro ogni route."""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Movie, Room

app = FastAPI(title="Cineteca API", version="0.4.0")


class RoomRead(BaseModel):
    room_id: int
    code: str
    name: str
    seats: int


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    director_id: int = Field(ge=1)
    release_year: int = Field(ge=1888, le=2100)
    runtime_min: int = Field(ge=1, le=600)
    purchase_price_eur: int = Field(ge=0)
    plot: str | None = Field(default=None, max_length=2000)


class MovieRead(BaseModel):
    movie_id: int
    title: str
    director_id: int
    release_year: int
    runtime_min: int
    plot: str | None


@app.get("/rooms")
def list_rooms() -> list[RoomRead]:
    query = select(Room).order_by(Room.room_id)
    with Session(engine) as session:
        return session.scalars(query).all()


@app.get(
    "/rooms/by-code/{code}",
    response_model=RoomRead,
    responses={404: {"description": "The room does not exist"}},
)
def get_room_by_code(code: str):
    query = select(Room).where(Room.code == code)
    with Session(engine) as session:
        room = session.scalars(query).one_or_none()
        if room is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"room {code} not found")
        return room


@app.get("/movies")
def list_movies(
    director_id: int | None = None,
    max_runtime: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[MovieRead]:
    query = select(Movie).order_by(Movie.movie_id)
    if director_id is not None:
        query = query.where(Movie.director_id == director_id)
    if max_runtime is not None:
        query = query.where(Movie.runtime_min <= max_runtime)
    if search is not None:
        query = query.where(Movie.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit)
    with Session(engine) as session:
        return session.scalars(query).all()


@app.get(
    "/movies/{movie_id}",
    response_model=MovieRead,
    responses={404: {"description": "The movie does not exist"}},
)
def get_movie(movie_id: int):
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie {movie_id} not found")
        return movie


@app.post(
    "/movies",
    status_code=status.HTTP_201_CREATED,
    response_model=MovieRead,
    responses={409: {"description": "Movie already in the catalogue or director_id not found"}},
)
def create_movie(data: MovieCreate):
    movie = Movie(**data.model_dump())
    with Session(engine) as session:
        session.add(movie)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="movie already in the catalogue or director_id not found",
            )
        session.refresh(movie)
        return movie


@app.put(
    "/movies/{movie_id}",
    response_model=MovieRead,
    responses={
        404: {"description": "The movie does not exist"},
        409: {"description": "Movie already in the catalogue or director_id not found"},
    },
)
def replace_movie(movie_id: int, data: MovieCreate):
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie {movie_id} not found")
        movie.title = data.title
        movie.director_id = data.director_id
        movie.release_year = data.release_year
        movie.runtime_min = data.runtime_min
        movie.purchase_price_eur = data.purchase_price_eur
        movie.plot = data.plot
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="movie already in the catalogue or director_id not found",
            )
        session.refresh(movie)
        return movie


@app.delete(
    "/movies/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "The movie does not exist"}},
)
def delete_movie(movie_id: int):
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie {movie_id} not found")
        session.delete(movie)
        session.commit()
