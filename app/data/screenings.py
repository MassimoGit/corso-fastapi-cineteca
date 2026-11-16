"""Il livello dati delle proiezioni: la lettura per il report."""
from sqlalchemy import Row, select
from sqlalchemy.orm import Session

from app.models import Movie, Room, Screening


def list_report_rows(session: Session) -> list[Row]:
    """Una riga per proiezione, con sala e titolo: data, codice sala, titolo, prezzo del biglietto."""
    statement = (
        select(Screening.starts_at, Room.code, Movie.title, Screening.ticket_price_eur)
        .join(Movie, Screening.movie_id == Movie.movie_id)
        .join(Room, Screening.room_id == Room.room_id)
        .order_by(Screening.starts_at)
    )
    return session.execute(statement).all()
