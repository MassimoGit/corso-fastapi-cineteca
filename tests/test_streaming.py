"""Le risposte in streaming: il report delle proiezioni, l'assistente finto e il lifespan."""
import asyncio
from datetime import datetime
from decimal import Decimal

from app.models import Screening
from app.services.assistant import fake_model


def test_report_without_screenings_has_only_the_header(client):
    response = client.get("/reports/screenings")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert response.text == "starts_at;room;title;ticket_price_eur\n"


def test_report_has_one_line_per_screening(client, session):
    session.add(Screening(movie_id=1, room_id=1, starts_at=datetime(2026, 11, 20, 20, 30), ticket_price_eur=Decimal("8.00")))
    session.flush()
    with client.stream("GET", "/reports/screenings") as response:
        lines = list(response.iter_lines())
    assert lines == ["starts_at;room;title;ticket_price_eur", "2026-11-20 20:30;S1;Interstellar;8.00"]


def test_report_rejects_a_pause_over_the_limit(client):
    assert client.get("/reports/screenings?pause_s=5").status_code == 422


def test_assistant_streams_the_whole_answer(client):
    response = client.get("/assistant/stream?question=ciao&delay_s=0")
    assert response.status_code == 200
    assert response.text.startswith("Hai chiesto: ciao. Questa risposta è finta")
    assert response.text.endswith("come in una chat. ")


def test_assistant_needs_a_question(client):
    assert client.get("/assistant/stream").status_code == 422


def test_fake_model_produces_one_word_at_a_time():
    async def collect() -> list[str]:
        return [word async for word in fake_model("ciao", 0)]

    words = asyncio.run(collect())
    assert words[:3] == ["Hai ", "chiesto: ", "ciao. "]
    assert len(words) > 10


def test_lifespan_runs_without_errors(client):
    # with: il TestClient esegue il lifespan, e allo spegnimento chiama engine.dispose()
    with client:
        assert client.get("/").status_code == 200
