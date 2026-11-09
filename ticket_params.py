"""I parametri con nome: i ticket chiusi di un cliente."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

query = text("""
    SELECT id_ticket, oggetto, priorita
    FROM ticket
    WHERE id_cliente = :customer_id AND stato = :status
    ORDER BY id_ticket
""")

with engine.connect() as conn:
    for customer_id in (3, 15):
        rows = conn.execute(query, {"customer_id": customer_id, "status": "chiuso"}).all()
        print(f"cliente {customer_id}: {len(rows)} ticket chiusi")
        for row in rows:
            print("  ", row.id_ticket, row.oggetto, f"({row.priorita})")
