"""Le righe che tornano da una query: tutte insieme, per nome, per posizione."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    result = conn.execute(text("SELECT id_cliente, ragione_sociale, citta FROM clienti ORDER BY ragione_sociale LIMIT 3"))
    rows = result.all()
    print("tipo:", type(rows).__name__, "- righe:", len(rows))

    row = rows[0]
    print("per nome:", row.ragione_sociale)
    print("per posizione:", row[2])
    customer_id, name, city = row
    print("spacchettata:", customer_id, name, city)

    print("seconda lettura dello stesso result:", result.all())
