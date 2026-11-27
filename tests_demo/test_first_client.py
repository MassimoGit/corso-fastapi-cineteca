"""Solo dimostrativo: la prima volta del TestClient, su routes che non toccano il database."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_info_returns_name_and_version():
    response = client.get("/")
    print("\n  ->", response.status_code, response.json())
    assert response.status_code == 200


def test_get_info_is_json():
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"


def test_get_movie_with_a_bad_id_returns_422():
    response = client.get("/movies/abc")
    print("\n  ->", response.status_code)
    print("  ->", response.json())
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["movie_id"]
