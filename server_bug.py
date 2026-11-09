"""Un errore nel nostro codice: il client riceve 500."""
from fastapi import FastAPI

app = FastAPI()

MOVIES = [
    {"movie_id": 1, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014},
    {"movie_id": 2, "title": "La vita è bella", "director": "Roberto Benigni", "release_year": 1997, "runtime_min": 116},
]


@app.get("/movies/total-runtime")
def total_runtime():
    return {"total_min": sum(m["runtime_min"] for m in MOVIES)}
