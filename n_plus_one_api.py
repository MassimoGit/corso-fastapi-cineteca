"""Errore comune: l'elenco dei film con il regista, senza caricarlo con la query. La serializzazione fa una query per film."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.dependencies import SessionDep
from app.models import Movie
from app.schemas import DirectorRead, MovieRead

app = FastAPI()


class MovieWithDirector(MovieRead):
    director: DirectorRead


@app.get("/movies-with-director")
def list_movies_with_director(session: SessionDep) -> list[MovieWithDirector]:
    return session.scalars(select(Movie).order_by(Movie.movie_id)).all()  # SBAGLIATO: il regista è caricato pigramente


if __name__ == "__main__":
    client = TestClient(app)
    response = client.get("/movies-with-director")
    print("GET /movies-with-director ->", response.status_code, "-", len(response.json()), "film")
