"""L'API della cineteca, prima versione: dati in memoria, solo letture."""
from datetime import datetime

from fastapi import FastAPI

app = FastAPI(
    title="Cineteca API",
    description="Film, sale e proiezioni della cineteca del corso.",
    version="0.1.0",
)

MOVIES = [
    {"movie_id": 1, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "runtime_min": 169},
    {"movie_id": 2, "title": "La vita è bella", "director": "Roberto Benigni", "release_year": 1997, "runtime_min": 116},
    {"movie_id": 3, "title": "Il buono, il brutto, il cattivo", "director": "Sergio Leone", "release_year": 1966, "runtime_min": 178},
    {"movie_id": 4, "title": "La città incantata", "director": "Hayao Miyazaki", "release_year": 2001, "runtime_min": 125},
    {"movie_id": 5, "title": "Inception", "director": "Christopher Nolan", "release_year": 2010, "runtime_min": 148},
]


@app.get("/")
def root():
    return {
        "service": "Cineteca API",
        "endpoints": {
            "GET /movies": "all movies",
            "GET /movies/directors": "number of movies per director",
            "GET /status": "current status of the cinema",
        },
    }


@app.get("/movies")
def list_movies():
    return MOVIES


@app.get("/movies/directors")
def count_by_director():
    counts = {}
    for movie in MOVIES:
        counts[movie["director"]] = counts.get(movie["director"], 0) + 1
    return counts


@app.get("/status")
def get_status():
    return {
        "is_open": True,
        "rooms": ("Sala Fellini", "Sala Leone", "Sala Wertmüller"),
        "next_screening_at": datetime(2026, 11, 6, 21, 15),
        "notice": None,
    }
