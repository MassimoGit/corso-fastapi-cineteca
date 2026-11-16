"""SBAGLIATO APPOSTA: il secondo test funziona solo se il primo è già girato."""

reviews = []  # SBAGLIATO: uno stato condiviso fra i test


def test_add_a_review():
    reviews.append("Bello, lo rivedrei volentieri.")
    assert len(reviews) == 1


def test_the_review_is_there():
    assert reviews[0] == "Bello, lo rivedrei volentieri."
