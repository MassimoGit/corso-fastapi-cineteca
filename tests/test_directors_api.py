"""I registi: creazione, duplicato e conteggio dei film."""


def test_create_director_returns_201(admin_client):
    response = admin_client.post("/directors", json={"name": "Denis Villeneuve"})
    assert response.status_code == 201
    assert response.json()["name"] == "Denis Villeneuve"


def test_create_director_twice_returns_409(admin_client):
    admin_client.post("/directors", json={"name": "Denis Villeneuve"})
    response = admin_client.post("/directors", json={"name": "Denis Villeneuve"})
    assert response.status_code == 409
    assert response.json() == {"detail": "director Denis Villeneuve already exists"}


def test_a_director_without_movies_counts_zero(admin_client):
    admin_client.post("/directors", json={"name": "Denis Villeneuve"})
    stats = admin_client.get("/stats/movies-per-director").json()
    assert stats == [
        {"director": "Christopher Nolan", "movies": 2},
        {"director": "Sergio Leone", "movies": 1},
        {"director": "Denis Villeneuve", "movies": 0},
    ]
