"""Un path parameter senza tipo: arriva come stringa."""
from fastapi import FastAPI

app = FastAPI()

MOVIES = [{"movie_id": 1, "title": "Interstellar"}, {"movie_id": 4, "title": "La città incantata"}]


@app.get("/movies/{movie_id}")
def get_movie(movie_id):
    print("movie_id:", repr(movie_id), type(movie_id))
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    return None
