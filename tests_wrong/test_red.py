"""SBAGLIATI APPOSTA: due test con l'aspettativa sbagliata, per leggere cosa dice pytest quando un assert fallisce."""
from app.schemas import MovieCreate, tidy_title


def test_tidy_title_collapses_spaces():
    assert tidy_title("  La   vita  è bella ") == "La vita e bella"  # SBAGLIATO: manca l'accento


def test_movie_create_keeps_the_values():
    movie = MovieCreate(
        title="Inception", director_id=1, release_year=2010, runtime_min=148, purchase_price_eur=1100
    )
    expected = {"title": "Inception", "director_id": 1, "release_year": 2010, "runtime_min": 150}  # SBAGLIATO: 150
    assert movie.model_dump(exclude={"plot", "purchase_price_eur"}) == expected
