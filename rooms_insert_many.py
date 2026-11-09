"""Più righe in una volta: una lista di dizionari come secondo argomento di execute."""
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

rooms = [
    {"code": "S6", "name": "Sala Visconti", "seats": 90},
    {"code": "S7", "name": "Sala Antonioni", "seats": 35},
]

# ON CONFLICT DO NOTHING salta le sale già presenti: lo script si può rilanciare.
insert = text("""
    INSERT INTO rooms (code, name, seats)
    VALUES (:code, :name, :seats)
    ON CONFLICT DO NOTHING
""")

with engine.begin() as conn:
    conn.execute(insert, rooms)

with engine.connect() as conn:
    for row in conn.execute(text("SELECT room_id, code, name, seats FROM rooms ORDER BY room_id")):
        print(row)
