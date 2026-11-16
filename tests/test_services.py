"""Un test sul livello dei servizi, senza HTTP: la regola e l'eccezione del dominio, con la Session di test."""
import pytest

from app.errors import MovieNotFoundError
from app.services import movies as movies_service


def test_get_movie_returns_the_movie(session):
    assert movies_service.get_movie(session, 1).title == "Interstellar"


def test_get_movie_raises_for_an_unknown_id(session):
    with pytest.raises(MovieNotFoundError, match="movie 999 not found"):
        movies_service.get_movie(session, 999)
