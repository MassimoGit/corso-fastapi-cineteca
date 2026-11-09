"""Elenca le sale della cineteca."""
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

with engine.connect() as conn:
    for row in conn.execute(text("SELECT room_id, code, name, seats FROM rooms ORDER BY room_id")):
        print(row)
