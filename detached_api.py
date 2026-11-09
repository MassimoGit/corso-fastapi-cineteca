"""Quando FastAPI chiude la Session rispetto alla serializzazione della risposta."""
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Movie
from app.schemas import DirectorRead, MovieRead

app = FastAPI()


class MovieWithDirector(MovieRead):
    director: DirectorRead


def get_session() -> Iterator[Session]:
    with Session(engine, expire_on_commit=False) as session:
        print("  dependency: apro la Session")
        yield session
        print("  dependency: chiudo la Session")


# Lo scope predefinito: la dependency si chiude dopo la risposta. scope="function": subito dopo la route.
DefaultSession = Annotated[Session, Depends(get_session)]
EarlySession = Annotated[Session, Depends(get_session, scope="function")]


@app.get("/default/{movie_id}")
def movie_default(movie_id: int, session: DefaultSession) -> MovieWithDirector:
    movie = session.get(Movie, movie_id)
    print("  route: restituisco il film")
    return movie


@app.get("/early/{movie_id}")
def movie_early(movie_id: int, session: EarlySession) -> MovieWithDirector:
    movie = session.get(Movie, movie_id)
    print("  route: restituisco il film")
    return movie


def find_movie(movie_id: int) -> Movie | None:
    """Una funzione dei dati che apre la propria Session, come in API06: SBAGLIATO con la Session di richiesta."""
    with Session(engine, expire_on_commit=False) as session:
        return session.get(Movie, movie_id)


@app.get("/own-session/{movie_id}")
def movie_own_session(movie_id: int) -> MovieWithDirector:
    movie = find_movie(movie_id)
    print("  route: restituisco il film, la sua Session è già chiusa")
    return movie


if __name__ == "__main__":
    client = TestClient(app)
    for path in ("/default/1", "/early/1"):
        print("GET", path)
        response = client.get(path)
        print("  ->", response.status_code, response.json()["director"])
    print("GET /own-session/1")
    try:
        client.get("/own-session/1")
    except Exception as error:
        problem = error.errors()[0]
        print("  ->", type(error).__name__, problem["loc"])
        print(" ", problem["msg"])
