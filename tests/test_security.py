"""La sicurezza essenziale: senza chiave, con la chiave sbagliata, con la chiave giusta."""
from sqlalchemy import func, select

from app.models import Movie, Spectator


def test_delete_movie_without_a_key_returns_401(client):
    response = client.delete("/movies/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
    assert response.headers["www-authenticate"] == "APIKey"


def test_delete_movie_with_a_wrong_key_returns_401(client):
    response = client.delete("/movies/1", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "invalid API key"}
    assert response.headers["www-authenticate"] == "APIKey"


def test_delete_movie_with_the_right_key_returns_204(admin_client):
    assert admin_client.delete("/movies/1").status_code == 204
    assert admin_client.get("/movies/1").status_code == 404


def test_a_refused_request_changes_nothing(client, session):
    client.delete("/movies/1")
    client.delete("/movies/1", headers={"X-API-Key": "wrong-key"})
    assert session.scalar(select(func.count()).select_from(Movie)) == 3


def test_a_key_with_non_ascii_characters_returns_401_not_500(client):
    # compare_digest su str solleverebbe TypeError: il confronto passa dai bytes
    response = client.delete("/movies/1", headers={"X-API-Key": "chiave-è".encode("utf-8")})
    assert response.status_code == 401


def test_reads_stay_open_without_a_key(client):
    assert client.get("/movies").status_code == 200
    assert client.get("/movies/1").status_code == 200
    assert client.get("/directors").status_code == 200


def test_every_write_route_is_protected(client, movie_data):
    requests = [
        client.post("/movies", json=movie_data),
        client.patch("/movies/1", json={"runtime_min": 170}),
        client.delete("/movies/1"),
        client.post("/directors", json={"name": "Denis Villeneuve"}),
        client.post("/spectators", json={"name": "luca_77"}),
    ]
    assert [response.status_code for response in requests] == [401, 401, 401, 401, 401]


def test_the_key_is_checked_before_the_body(client):
    # un corpo non valido e nessuna chiave: risponde 401, non 422 (non dice niente a chi non è autorizzato)
    response = client.post("/movies", json={"title": 5})
    assert response.status_code == 401


def test_create_spectator_returns_the_token_once(admin_client, client, session):
    response = admin_client.post("/spectators", json={"name": "luca_77"})
    assert response.status_code == 201
    card = response.json()
    assert card["name"] == "luca_77"
    assert len(card["token"]) == 43
    assert session.scalar(select(Spectator.name).where(Spectator.token == card["token"])) == "luca_77"
    # il token appena creato apre la porta delle recensioni
    review = client.post(
        "/movies/2/reviews",
        json={"rating": 5, "text": "Lo rivedrei ogni anno."},
        headers={"Authorization": f"Bearer {card['token']}"},
    )
    assert review.status_code == 201
    assert review.json()["author"] == "luca_77"


def test_create_spectator_twice_returns_409(admin_client):
    assert admin_client.post("/spectators", json={"name": "luca_77"}).status_code == 201
    response = admin_client.post("/spectators", json={"name": "luca_77"})
    assert response.status_code == 409
    assert response.json() == {"detail": "spectator luca_77 already exists"}


def test_every_spectator_gets_a_different_token(admin_client):
    first = admin_client.post("/spectators", json={"name": "luca_77"}).json()["token"]
    second = admin_client.post("/spectators", json={"name": "anna_film"}).json()["token"]
    assert first != second
