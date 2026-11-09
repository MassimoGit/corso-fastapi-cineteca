"""Un valore solo, righe come dizionari, e i tipi Python delle colonne."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    total = conn.execute(text("SELECT count(*) FROM clienti")).scalar()
    print("scalar():", total)

    dicts = conn.execute(text("SELECT id_cliente, ragione_sociale FROM clienti ORDER BY id_cliente LIMIT 2")).mappings().all()
    print("mappings():", dicts)

    ticket = conn.execute(text("SELECT importo, aperto_il FROM ticket WHERE id_ticket = 1")).first()
    print("tipi:", type(ticket.importo).__name__, type(ticket.aperto_il).__name__)
