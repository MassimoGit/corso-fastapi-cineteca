"""Senza un modello in uscita, tutto quello che c'è nel dizionario finisce nella risposta."""
from fastapi import FastAPI

app = FastAPI()

MOVIES = [
    {"movie_id": 1, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "runtime_min": 169, "purchase_price_eur": 1200},
]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    return None
