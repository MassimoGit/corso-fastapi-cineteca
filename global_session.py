"""Errore comune: una sola Session per tutto il programma. Una richiesta che fallisce rovina anche le successive."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import engine
from app.errors import register_error_handlers
from app.schemas import MovieCreate, MovieRead
from app.services import movies as movies_service

app = FastAPI()
register_error_handlers(app)

session = Session(engine)  # SBAGLIATO: creata una volta sola, condivisa da tutte le richieste


@app.get("/movies")
def list_movies() -> list[MovieRead]:
    return movies_service.list_movies(session, None, None, None, 0, 20)


@app.post("/movies", status_code=201)
def create_movie(movie: MovieCreate) -> MovieRead:
    return movies_service.create_movie(session, movie)


if __name__ == "__main__":
    client = TestClient(app)
    inception = {"title": "Inception", "director_id": 1, "release_year": 2010,
                 "runtime_min": 148, "purchase_price_eur": 1100}

    response = client.get("/movies")
    print("1. GET /movies ->", response.status_code, "-", len(response.json()), "film")

    response = client.post("/movies", json=inception)
    print("2. POST /movies (duplicato) ->", response.status_code, "-", response.text)

    try:
        client.get("/movies")
    except Exception as error:
        print("3. GET /movies ->", type(error).__name__)
        print(error)
