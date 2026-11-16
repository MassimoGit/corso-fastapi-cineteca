"""SBAGLIATO APPOSTA: i test usano la get_session vera dell'app, senza override. conftest.py di questa cartella
fa le veci del database vero con uno schema d'appoggio che resta dopo i test, come resterebbe cineteca."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_directors_start_empty():
    assert client.get("/directors").json() == []


def test_create_director():
    response = client.post("/directors", json={"name": "Denis Villeneuve"})
    assert response.status_code == 201
