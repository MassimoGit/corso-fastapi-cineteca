"""Gestire l'errore: IntegrityError e l'eccezione del driver che sta dentro (e.orig)."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"options": "-c search_path=cineteca,public"},
)

INSERT = text("INSERT INTO rooms (code, name, seats) VALUES (:code, :name, :seats)")

attempts = [
    {"code": "S10", "name": "Sala Moretti", "seats": 0},
    {"code": "S1", "name": "Sala Fellini bis", "seats": 80},
]

for room in attempts:
    try:
        with engine.begin() as conn:
            conn.execute(INSERT, room)
    except IntegrityError as error:
        print("sala", room["code"], "rifiutata")
        print("  eccezione del driver:", type(error.orig).__name__)
        print("  constraint violato:", error.orig.diag.constraint_name)
        print("  messaggio:", str(error.orig).splitlines()[0])
    else:
        print("sala", room["code"], "inserita")

with engine.connect() as conn:
    print("sale in tabella:", conn.execute(text("SELECT count(*) FROM rooms")).scalar())
