"""Solo dimostrativo: l'ordine di una fixture con yield, anche quando il test fallisce."""
import pytest


@pytest.fixture
def open_cinema():
    print("\n  1. fixture: preparo")
    yield "aperto"
    print("\n  3. fixture: pulisco")


def test_cinema_is_open(open_cinema):
    print("\n  2. test: lavoro")
    assert open_cinema == "aperto"


def test_cinema_is_closed(open_cinema):
    print("\n  2. test: lavoro, poi fallisco")
    assert open_cinema == "chiuso"
