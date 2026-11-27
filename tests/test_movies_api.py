"""Le routes dei film, provate con il TestClient sullo schema cineteca_test.

I dati di partenza (conftest.py): 1 Interstellar, 2 Inception (Nolan), 3 Il buono, il brutto, il cattivo (Leone).
"""
from sqlalchemy import func, select

from app.models import Review


def test_list_movies_returns_the_catalogue(client):
    response = client.get("/movies")
    assert response.status_code == 200
    titles = [movie["title"] for movie in response.json()]
    assert titles == ["Interstellar", "Inception", "Il buono, il brutto, il cattivo"]


def test_list_movies_filters_by_max_runtime(client):
    response = client.get("/movies", params={"max_runtime": 150})
    assert [movie["title"] for movie in response.json()] == ["Inception"]


def test_get_movie_returns_the_movie(client):
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {
        "title": "Interstellar",
        "director_id": 1,
        "release_year": 2014,
        "runtime_min": 169,
        "plot": None,
        "movie_id": 1,
    }


def test_get_movie_returns_404_for_an_unknown_id(client):
    response = client.get("/movies/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "movie 999 not found"}


def test_get_movie_returns_422_for_an_id_that_is_not_a_number(client):
    response = client.get("/movies/abc")
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["movie_id"]


def test_create_movie_returns_201_and_the_movie_can_be_read_back(admin_client, movie_data):
    response = admin_client.post("/movies", json=movie_data)
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == "La città incantata"
    assert admin_client.get(f"/movies/{created['movie_id']}").json() == created


def test_create_movie_twice_returns_409(admin_client, movie_data):
    assert admin_client.post("/movies", json=movie_data).status_code == 201
    response = admin_client.post("/movies", json=movie_data)
    assert response.status_code == 409
    assert response.json() == {"detail": "movie already in the catalogue or director_id not found"}


def test_create_movie_with_an_unknown_director_returns_409(admin_client, movie_data):
    movie_data["director_id"] = 99
    assert admin_client.post("/movies", json=movie_data).status_code == 409


def test_the_catalogue_still_works_after_a_409(admin_client, movie_data):
    movie_data["director_id"] = 99
    assert admin_client.post("/movies", json=movie_data).status_code == 409
    assert admin_client.get("/movies").status_code == 200


def test_create_movie_with_an_invalid_year_returns_422(admin_client, movie_data):
    movie_data["release_year"] = 1500
    response = admin_client.post("/movies", json=movie_data)
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["release_year"]


def test_update_movie_changes_only_the_given_field(admin_client):
    response = admin_client.patch("/movies/1", json={"runtime_min": 170})
    assert response.status_code == 200
    assert response.json()["runtime_min"] == 170
    assert response.json()["title"] == "Interstellar"


def test_delete_movie_also_deletes_its_reviews(admin_client, session):
    reviews_before = session.scalar(select(func.count()).select_from(Review).where(Review.movie_id == 1))
    assert reviews_before == 1
    assert admin_client.delete("/movies/1").status_code == 204
    assert admin_client.get("/movies/1").status_code == 404
    assert session.scalar(select(func.count()).select_from(Review).where(Review.movie_id == 1)) == 0


def test_get_movie_detail_has_director_and_cast(client):
    detail = client.get("/movies/1/detail").json()
    assert detail["director"]["name"] == "Christopher Nolan"
    assert [(role["actor"]["name"], role["character_name"]) for role in detail["cast"]] == [
        ("Matthew McConaughey", "Joseph Cooper")
    ]
