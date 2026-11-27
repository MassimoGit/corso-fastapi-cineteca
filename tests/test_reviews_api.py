"""Le recensioni: l'autore è lo spettatore dell'header X-Spectator, scelto fra le tessere delle Settings.

Le tessere dei test sono quelle di test_settings (conftest.py): tester e other_tester.
"""

TESTER = {"X-Spectator": "tester"}
REVIEW = {"rating": 4, "text": "Bello, lo rivedrei volentieri."}


def test_create_review_uses_the_spectator_as_author(client):
    response = client.post("/movies/2/reviews", json=REVIEW, headers=TESTER)
    assert response.status_code == 201
    assert response.json()["author"] == "tester"
    assert response.json()["movie_id"] == 2


def test_create_review_without_the_header_returns_422(client):
    response = client.post("/movies/2/reviews", json=REVIEW)
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["x-spectator"]


def test_create_review_with_an_unknown_spectator_returns_401(client):
    # giulia_88 è fra le tessere dell'app vera, ma non fra quelle dei test
    response = client.post("/movies/2/reviews", json=REVIEW, headers={"X-Spectator": "giulia_88"})
    assert response.status_code == 401
    assert response.json() == {"detail": "unknown spectator giulia_88"}


def test_create_review_for_an_unknown_movie_returns_404(client):
    response = client.post("/movies/999/reviews", json=REVIEW, headers=TESTER)
    assert response.status_code == 404


def test_create_review_with_a_rating_out_of_range_returns_422(client):
    response = client.post("/movies/2/reviews", json={**REVIEW, "rating": 6}, headers=TESTER)
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["rating"]


def test_create_review_rejects_a_text_made_of_spaces(client):
    response = client.post("/movies/2/reviews", json={"rating": 4, "text": " " * 12}, headers=TESTER)
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["text"]


def test_list_reviews_returns_the_reviews_of_the_movie(client):
    response = client.get("/movies/1/reviews")
    assert response.status_code == 200
    assert [review["author"] for review in response.json()] == ["giulia_88"]
