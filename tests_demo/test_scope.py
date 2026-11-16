"""Solo dimostrativo: quante volte vive una fixture, secondo lo scope."""
import pytest


@pytest.fixture(scope="session")
def ticket_office():
    print("\n  [session] apro la biglietteria")
    yield "biglietteria"
    print("\n  [session] chiudo la biglietteria")


@pytest.fixture
def ticket(ticket_office):
    print("\n  [function] stacco un biglietto")
    return f"biglietto della {ticket_office}"


def test_first_ticket(ticket):
    print("\n  test 1")


def test_second_ticket(ticket):
    print("\n  test 2")
