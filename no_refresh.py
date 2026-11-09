"""Errore da non fare: restituire l'oggetto dopo il commit, senza session.refresh."""
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import engine
from models import Movie

app = FastAPI()


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


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(data: MovieCreate) -> MovieRead:
    movie = Movie(**data.model_dump())
    with Session(engine) as session:
        session.add(movie)
        session.commit()
        return movie  # SBAGLIATO: manca session.refresh(movie) dopo il commit
