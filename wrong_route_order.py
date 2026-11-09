"""Errore comune: la route con il parametro dichiarata prima di quella fissa."""
from fastapi import FastAPI

app = FastAPI()

MOVIES = [{"movie_id": 1, "title": "Interstellar"}, {"movie_id": 2, "title": "La vita è bella"}]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    return None


@app.get("/movies/directors")
def count_directors():
    return {"movies": len(MOVIES)}
