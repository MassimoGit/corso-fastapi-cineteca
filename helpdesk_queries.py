"""La prima query: i primi tre clienti dell'helpdesk, in ordine alfabetico."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

query = text("SELECT id_cliente, ragione_sociale, piano FROM clienti ORDER BY ragione_sociale LIMIT 3")

with engine.connect() as conn:
    result = conn.execute(query)
    for row in result:
        print(row)
