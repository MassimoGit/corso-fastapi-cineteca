"""Errore comune: return al posto di raise."""
from fastapi import FastAPI, HTTPException

app = FastAPI()

MOVIES = [{"movie_id": 1, "title": "Interstellar"}]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    return HTTPException(status_code=404, detail=f"movie {movie_id} not found")
