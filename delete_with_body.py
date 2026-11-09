"""Errore comune: un corpo nella risposta 204."""
from fastapi import FastAPI

app = FastAPI()

MOVIES = [{"movie_id": 1, "title": "Interstellar"}]


@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int):
    MOVIES.clear()
    return {"deleted": movie_id}
