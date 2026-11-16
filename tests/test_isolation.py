"""Ogni test parte dai dati di partenza: quello che un test scrive, anche con un commit, non arriva al successivo."""


def test_first_writes_a_director_and_the_route_commits(client):
    response = client.post("/directors", json={"name": "Denis Villeneuve"})
    assert response.status_code == 201
    assert len(client.get("/directors").json()) == 3


def test_second_sees_only_the_starting_data(client):
    assert len(client.get("/directors").json()) == 2


def test_earlier_work_survives_a_409(client, movie_data):
    """Un errore della route (e il suo rollback) non deve portarsi via quello che il test ha fatto prima."""
    created = client.post("/movies", json=movie_data)
    assert created.status_code == 201
    movie_data["director_id"] = 99
    assert client.post("/movies", json=movie_data).status_code == 409
    assert client.get(f"/movies/{created.json()['movie_id']}").status_code == 200
