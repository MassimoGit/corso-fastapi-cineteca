"""Tutto o niente: la seconda sala viola il CHECK, e nemmeno la prima resta."""
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

new_rooms = [
    {"code": "S9", "name": "Sala De Sica", "seats": 50},
    {"code": "S10", "name": "Sala Moretti", "seats": 0},
]

with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO rooms (code, name, seats) VALUES (:code, :name, :seats)"),
        new_rooms,
    )
