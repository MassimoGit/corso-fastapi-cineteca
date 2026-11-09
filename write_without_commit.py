"""Scrivere senza commit: la modifica sparisce alla chiusura della connection."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))
SEATS = text("SELECT seats FROM cineteca.rooms WHERE code = 'S1'")

with engine.connect() as conn:
    conn.execute(text("UPDATE cineteca.rooms SET seats = 130 WHERE code = 'S1'"))
    print("dentro il blocco, posti della sala S1:", conn.execute(SEATS).scalar())

with engine.connect() as conn:
    print("in una nuova connection, posti della sala S1:", conn.execute(SEATS).scalar())
