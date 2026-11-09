"""engine.begin(): la transaction in un blocco, commit alla fine o rollback se c'è un'eccezione."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"options": "-c search_path=cineteca,public"},
)

UPDATE = text("UPDATE rooms SET seats = :seats WHERE code = :code")


def seats(code):
    query = text("SELECT seats FROM rooms WHERE code = :code")
    with engine.connect() as conn:
        return conn.execute(query, {"code": code}).scalar()


print("all'inizio, posti di S1:", seats("S1"), "- posti di S2:", seats("S2"))

# Primo blocco: arriva in fondo senza errori, quindi parte il commit.
with engine.begin() as conn:
    conn.execute(UPDATE, {"code": "S1", "seats": 130})
print("dopo il primo blocco, posti di S1:", seats("S1"))

# Secondo blocco: l'eccezione esce dal blocco, quindi parte il rollback.
try:
    with engine.begin() as conn:
        conn.execute(UPDATE, {"code": "S2", "seats": 70})
        raise RuntimeError("qualcosa è andato storto")
except RuntimeError as error:
    print("errore:", error)
print("dopo il secondo blocco, posti di S2:", seats("S2"))

# Pulizia, così lo script si può rilanciare.
with engine.begin() as conn:
    conn.execute(UPDATE, {"code": "S1", "seats": 120})
