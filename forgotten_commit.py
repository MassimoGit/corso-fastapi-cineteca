"""Il commit dimenticato: nessun errore, ma la sala non c'è."""
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
    conn.execute(text("INSERT INTO rooms (code, name, seats) VALUES ('S11', 'Sala dimenticata', 30)"))
    print("dentro il blocco:", conn.execute(text("SELECT count(*) FROM rooms WHERE code = 'S11'")).scalar())

with engine.connect() as conn:
    print("dopo il blocco:", conn.execute(text("SELECT count(*) FROM rooms WHERE code = 'S11'")).scalar())
