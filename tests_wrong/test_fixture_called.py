"""SBAGLIATO APPOSTA: la fixture è chiamata come una funzione normale."""
import pytest

from app.schemas import MovieCreate


@pytest.fixture
def movie_data() -> dict:
    return {"title": "Inception", "director_id": 1, "release_year": 2010, "runtime_min": 148, "purchase_price_eur": 1100}


def test_movie_create_accepts_the_data():
    data = movie_data()  # SBAGLIATO: pytest passa la fixture come parametro, non si chiama
    assert MovieCreate(**data).title == "Inception"
