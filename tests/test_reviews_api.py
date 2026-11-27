"""Le recensioni: l'autore è lo spettatore a cui appartiene il token dell'header Authorization: Bearer.

I token dei test sono quelli che conftest.py scrive nel database di prova: giulia-test-token e marco-test-token.
"""

GIULIA = {"Authorization": "Bearer giulia-test-token"}
REVIEW = {"rating": 4, "text": "Bello, lo rivedrei volentieri."}


def test_create_review_uses_the_spectator_as_author(client):
    response = client.post("/movies/2/reviews", json=REVIEW, headers=GIULIA)
    assert response.status_code == 201
    assert response.json()["author"] == "giulia_88"
    assert response.json()["movie_id"] == 2


def test_create_review_without_the_token_returns_401(client):
    response = client.post("/movies/2/reviews", json=REVIEW)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_create_review_with_an_unknown_token_returns_401(client):
    # il nome di uno spettatore non è il suo token: scriverlo nell'header non serve più
    response = client.post("/movies/2/reviews", json=REVIEW, headers={"Authorization": "Bearer giulia_88"})
    assert response.status_code == 401
    assert response.json() == {"detail": "invalid spectator token"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_create_review_with_another_scheme_returns_401(client):
    # il token c'è, ma con lo schema Basic: HTTPBearer non lo guarda nemmeno
    response = client.post("/movies/2/reviews", json=REVIEW, headers={"Authorization": "Basic giulia-test-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_create_review_with_a_token_without_the_scheme_returns_401(client):
    response = client.post("/movies/2/reviews", json=REVIEW, headers={"Authorization": "giulia-test-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_the_bearer_scheme_name_is_not_case_sensitive(client):
    response = client.post("/movies/2/reviews", json=REVIEW, headers={"Authorization": "bearer giulia-test-token"})
    assert response.status_code == 201


def test_create_review_for_an_unknown_movie_returns_404(client):
    response = client.post("/movies/999/reviews", json=REVIEW, headers=GIULIA)
    assert response.status_code == 404


def test_create_review_with_a_rating_out_of_range_returns_422(client):
    response = client.post("/movies/2/reviews", json={**REVIEW, "rating": 6}, headers=GIULIA)
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["rating"]


def test_create_review_rejects_a_text_made_of_spaces(client):
    response = client.post("/movies/2/reviews", json={"rating": 4, "text": " " * 12}, headers=GIULIA)
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["text"]


def test_list_reviews_returns_the_reviews_of_the_movie(client):
    response = client.get("/movies/1/reviews")
    assert response.status_code == 200
    assert [review["author"] for review in response.json()] == ["giulia_88"]
