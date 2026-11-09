"""Un segnaposto senza il suo valore: la query non parte."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

query = text("SELECT id_ticket, oggetto FROM ticket WHERE id_cliente = :customer_id")

with engine.connect() as conn:
    rows = conn.execute(query).all()
