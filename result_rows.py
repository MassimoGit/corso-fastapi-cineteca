"""Le righe che tornano da una query: per nome, per posizione, come dizionari."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import MultipleResultsFound

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    result = conn.execute(text("SELECT id_cliente, ragione_sociale, citta FROM clienti ORDER BY ragione_sociale LIMIT 3"))
    rows = result.all()
    print("tipo:", type(rows).__name__, "- righe:", len(rows))

    row = rows[0]
    print("riga intera:", row)
    print("per nome:", row.ragione_sociale)
    print("per posizione:", row[2])
    customer_id, name, city = row
    print("spacchettata:", customer_id, name, city)

    print("seconda lettura dello stesso result:", result.all())

    first = conn.execute(text("SELECT ragione_sociale FROM clienti ORDER BY ragione_sociale")).first()
    print("first():", first)

    one = conn.execute(text("SELECT ragione_sociale, piano FROM clienti WHERE id_cliente = 3")).one()
    print("one():", one)

    try:
        conn.execute(text("SELECT ragione_sociale FROM clienti WHERE piano = 'Premium'")).one()
    except MultipleResultsFound as error:
        print("one() con più righe:", error)

    dicts = conn.execute(text("SELECT id_cliente, ragione_sociale FROM clienti ORDER BY id_cliente LIMIT 2")).mappings().all()
    print("dizionari:", dicts)
    print("il primo:", dict(dicts[0]))

    ticket = conn.execute(text("SELECT importo, aperto_il FROM ticket WHERE id_ticket = 1")).one()
    print("tipi:", type(ticket.importo).__name__, type(ticket.aperto_il).__name__)
