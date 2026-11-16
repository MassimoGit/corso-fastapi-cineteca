"""SBAGLIATO APPOSTA: un caso su quattro ha l'aspettativa sbagliata."""
import pytest

from app.schemas import tidy_title


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Interstellar", "Interstellar"),
        ("  Inception ", "Inception"),
        ("Il  buono,  il brutto", "Il buono il brutto"),  # SBAGLIATO: manca la virgola
        ("Il  postino\n", "Il postino"),
    ],
)
def test_tidy_title_cleans_the_title(raw, expected):
    assert tidy_title(raw) == expected
