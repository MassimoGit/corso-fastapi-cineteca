"""SBAGLIATO APPOSTA: il primo test lascia un override attivo, e il secondo ne paga le conseguenze."""
from fastapi.testclient import TestClient

from app.database import Settings, get_settings
from app.main import app

client = TestClient(app)


def test_a_uses_other_settings():
    app.dependency_overrides[get_settings] = lambda: Settings(app_name="Cinema di prova")  # SBAGLIATO: nessuna pulizia
    assert client.get("/").json()["name"] == "Cinema di prova"


def test_b_expects_the_real_settings():
    assert client.get("/").json()["name"] == "Cineteca API"
