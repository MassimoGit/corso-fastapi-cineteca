"""La sicurezza: chiave di servizio per /spectators e Bearer JWT con ruoli per il catalogo."""
from sqlalchemy import func, select

from app.models import Movie, Spectator


def test_create_spectator_without_a_key_returns_401(client):
    response = client.post("/spectators", json={"name": "luca_77"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["www-authenticate"] == "APIKey"


def test_create_spectator_with_a_wrong_key_returns_401(client):
    response = client.post("/spectators", json={"name": "luca_77"}, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "invalid API key"}
    assert response.headers["www-authenticate"] == "APIKey"


def test_a_key_with_non_ascii_characters_returns_401_not_500(client):
    response = client.post(
        "/spectators", json={"name": "luca_77"}, headers={"X-API-Key": "chiave-è".encode("utf-8")}
    )
    assert response.status_code == 401


def test_delete_movie_without_a_token_returns_401(client):
    response = client.delete("/movies/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_staff_can_create_and_update_a_movie_but_cannot_delete_it(staff_client, movie_data):
    created = staff_client.post("/movies", json=movie_data)
    assert created.status_code == 201
    movie_id = created.json()["movie_id"]
    assert staff_client.patch(f"/movies/{movie_id}", json={"runtime_min": 130}).status_code == 200
    deleted = staff_client.delete(f"/movies/{movie_id}")
    assert deleted.status_code == 403
    assert deleted.json() == {"detail": "admin role required"}


def test_delete_movie_with_admin_jwt_returns_204(admin_client):
    assert admin_client.delete("/movies/1").status_code == 204
    assert admin_client.get("/movies/1").status_code == 404


def test_a_refused_request_changes_nothing(client, staff_client, session):
    client.delete("/movies/1")
    staff_client.delete("/movies/1")
    assert session.scalar(select(func.count()).select_from(Movie)) == 3


def test_reads_stay_open_without_a_token(client):
    assert client.get("/movies").status_code == 200
    assert client.get("/movies/1").status_code == 200
    assert client.get("/directors").status_code == 200
    assert client.get("/catalogue").status_code == 200


def test_every_protected_route_refuses_anonymous_caller(client, movie_data):
    requests = [
        client.post("/movies", json=movie_data),
        client.patch("/movies/1", json={"runtime_min": 170}),
        client.delete("/movies/1"),
        client.post("/directors", json={"name": "Denis Villeneuve"}),
        client.post("/spectators", json={"name": "luca_77"}),
        client.get("/users/me"),
        client.get("/users"),
        client.get("/stats/movies-per-director"),
    ]
    assert [response.status_code for response in requests] == [401, 401, 401, 401, 401, 401, 401, 401]


def test_the_token_is_checked_before_the_body(client):
    # un corpo non valido senza Bearer token risponde 401, non 422
    response = client.post("/movies", json={"title": 5})
    assert response.status_code == 401


def test_create_spectator_returns_the_token_once(api_key_client, client, session):
    response = api_key_client.post("/spectators", json={"name": "luca_77"})
    assert response.status_code == 201
    card = response.json()
    assert card["name"] == "luca_77"
    assert len(card["token"]) == 43
    assert session.scalar(select(Spectator.name).where(Spectator.token == card["token"])) == "luca_77"
    review = client.post(
        "/movies/2/reviews",
        json={"rating": 5, "text": "Lo rivedrei ogni anno."},
        headers={"Authorization": f"Bearer {card['token']}"},
    )
    assert review.status_code == 201
    assert review.json()["author"] == "luca_77"


def test_create_spectator_twice_returns_409(api_key_client):
    assert api_key_client.post("/spectators", json={"name": "luca_77"}).status_code == 201
    response = api_key_client.post("/spectators", json={"name": "luca_77"})
    assert response.status_code == 409
    assert response.json() == {"detail": "spectator luca_77 already exists"}


def test_every_spectator_gets_a_different_token(api_key_client):
    first = api_key_client.post("/spectators", json={"name": "luca_77"}).json()["token"]
    second = api_key_client.post("/spectators", json={"name": "anna_film"}).json()["token"]
    assert first != second
