"""Errore comune: PATCH senza exclude_unset. I campi non mandati diventano None."""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import engine
from models import Movie

app = FastAPI()


class MovieRead(BaseModel):
    movie_id: int
    title: str
    director_id: int
    release_year: int
    runtime_min: int
    plot: str | None


class MovieUpdate(BaseModel):
    title: str | None = None
    director_id: int | None = None
    release_year: int | None = None
    runtime_min: int | None = None
    purchase_price_eur: int | None = None
    plot: str | None = None


@app.patch("/movies/{movie_id}")
def update_movie(movie_id: int, changes: MovieUpdate) -> MovieRead:
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie {movie_id} not found")
        for name, value in changes.model_dump().items():  # manca exclude_unset=True
            setattr(movie, name, value)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="movie already in the catalogue or director_id not found")
        session.refresh(movie)
        return movie
