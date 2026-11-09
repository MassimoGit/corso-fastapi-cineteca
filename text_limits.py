"""I limiti di text(): il SQL è una stringa, e le righe non hanno un tipo Python tutto loro."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"options": "-c search_path=cineteca,public"},
)


def list_rooms(conn):
    """Restituisce le sale come dizionari: la conversione riga per riga è a carico nostro."""
    rows = conn.execute(text("SELECT room_id, code, name, seats FROM rooms ORDER BY room_id"))
    return [{"room_id": r.room_id, "code": r.code, "name": r.name, "seats": r.seats} for r in rows]


def big_rooms(conn, min_seats):
    """Lo stesso SELECT, scritto di nuovo in un'altra stringa, con un errore di battitura."""
    rows = conn.execute(text("SELECT room_id, name FROM rooms WHERE sets >= :min_seats"), {"min_seats": min_seats})
    return rows.all()


with engine.connect() as conn:
    for room in list_rooms(conn):
        print(room)

with engine.connect() as conn:
    try:
        big_rooms(conn, 50)
    except ProgrammingError as error:
        print("errore trovato solo adesso, a programma avviato:")
        print(str(error.orig).splitlines()[0])
