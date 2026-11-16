"""I test dei pezzi senza HTTP: la funzione tidy_title e gli schemi Pydantic di app/schemas.py."""
import pytest
from pydantic import ValidationError

from app.schemas import MovieCreate, MovieUpdate, tidy_title


def test_tidy_title_collapses_spaces():
    assert tidy_title("  La   vita  è bella ") == "La vita è bella"


def test_tidy_title_rejects_a_blank_title():
    with pytest.raises(ValueError, match="title cannot be blank"):
        tidy_title("   ")


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Interstellar", "Interstellar"),
        ("  Inception ", "Inception"),
        ("Il  buono,  il brutto", "Il buono, il brutto"),
        ("Il  postino\n", "Il postino"),
    ],
)
def test_tidy_title_cleans_the_title(raw, expected):
    assert tidy_title(raw) == expected


@pytest.mark.parametrize("blank", ["", "   ", "\t\n"])
def test_tidy_title_rejects_every_kind_of_blank(blank):
    with pytest.raises(ValueError):
        tidy_title(blank)


def test_movie_create_cleans_the_title(movie_data):
    movie_data["title"] = "  Inception  "
    movie = MovieCreate(**movie_data)
    assert movie.title == "Inception"


def test_movie_create_rejects_a_year_before_cinema(movie_data):
    movie_data["release_year"] = 1500
    with pytest.raises(ValidationError) as error:
        MovieCreate(**movie_data)
    first = error.value.errors()[0]
    assert first["loc"] == ("release_year",)
    assert first["type"] == "greater_than_equal"


def test_movie_update_rejects_a_null_title():
    with pytest.raises(ValidationError, match="title cannot be null"):
        MovieUpdate(title=None)
