"""Il report delle proiezioni, scritto una riga alla volta."""
import time
from collections.abc import Iterator

from sqlalchemy import Row
from sqlalchemy.orm import Session

from app.data import screenings as screenings_data


def list_screening_rows(session: Session) -> list[Row]:
    return screenings_data.list_report_rows(session)


def report_lines(rows: list[Row], pause_s: float) -> Iterator[str]:
    """Un generatore: produce l'intestazione e poi una riga per proiezione, con una pausa che simula un report lungo."""
    yield "starts_at;room;title;ticket_price_eur\n"
    for starts_at, room_code, title, price in rows:
        time.sleep(pause_s)
        yield f"{starts_at:%Y-%m-%d %H:%M};{room_code};{title};{price}\n"
