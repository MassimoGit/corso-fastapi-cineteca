"""echo=True: il SQL che parte davvero verso il server."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

query = text("SELECT id_ticket, oggetto FROM ticket WHERE id_cliente = 3 ORDER BY id_ticket LIMIT 2")

with engine.connect() as conn:
    rows = conn.execute(query).all()
    print(rows)
