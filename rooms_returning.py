"""RETURNING: l'id deciso dal database torna subito in Python."""
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

room = {"code": "S8", "name": "Sala Bertolucci", "seats": 55}

with engine.begin() as conn:
    # Prima si toglie la sala, se c'è già: così lo script si può rilanciare.
    conn.execute(text("DELETE FROM rooms WHERE code = :code"), {"code": room["code"]})

    row = conn.execute(
        text("""
            INSERT INTO rooms (code, name, seats)
            VALUES (:code, :name, :seats)
            RETURNING room_id, code, name || ' (' || seats || ' posti)' AS label
        """),
        room,
    ).one()
    print("riga inserita:", row)
    print("room_id:", row.room_id)
    print("etichetta:", row.label)

    new_id = conn.execute(
        text("INSERT INTO rooms (code, name, seats) VALUES ('S9', 'Sala prova', 10) RETURNING room_id")
    ).scalar()
    print("solo l'id:", new_id)
    conn.execute(text("DELETE FROM rooms WHERE room_id = :room_id"), {"room_id": new_id})
