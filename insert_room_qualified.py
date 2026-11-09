"""Una scrittura con il nome qualificato: una sala nuova nella tabella cineteca.rooms."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

room = {"code": "S5", "name": "Sala Rossellini", "seats": 80}

with engine.begin() as conn:
    # Prima si toglie la sala, se c'è già: così lo script si può rilanciare.
    conn.execute(text("DELETE FROM cineteca.rooms WHERE code = :code"), {"code": room["code"]})
    result = conn.execute(
        text("INSERT INTO cineteca.rooms (code, name, seats) VALUES (:code, :name, :seats)"),
        room,
    )
    print("righe inserite:", result.rowcount)

with engine.connect() as conn:
    for row in conn.execute(text("SELECT room_id, code, name, seats FROM cineteca.rooms ORDER BY room_id")):
        print(row)
