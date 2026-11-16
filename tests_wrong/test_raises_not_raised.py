"""SBAGLIATO APPOSTA: il test aspetta un'eccezione che il codice non solleva."""
import pytest

from app.schemas import tidy_title


def test_tidy_title_rejects_a_blank_title():
    with pytest.raises(ValueError):
        tidy_title("Inception")  # SBAGLIATO: il titolo non è vuoto, nessuna eccezione
