"""La risposta non rispetta il modello dichiarato: 500 e ResponseValidationError nel log."""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class MovieRead(BaseModel):
    movie_id: int
    title: str
    runtime_min: int


MOVIES = [{"movie_id": 1, "title": "Interstellar", "runtime": 169}]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int) -> MovieRead:
    return MOVIES[0]
