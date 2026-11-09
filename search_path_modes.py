"""Tre modi di indicare lo schema: la stessa SELECT, che trova o non trova la tabella movies."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
COUNT = text("SELECT count(*) FROM movies")
engine = create_engine(DATABASE_URL)

# Senza niente: il search_path del ruolo non contiene lo schema cineteca.
with engine.connect() as conn:
    try:
        conn.execute(COUNT)
    except Exception as error:
        print("0. senza niente:", type(error.orig).__name__ + ":", str(error.orig).splitlines()[0])

# Primo modo: il nome qualificato, schema punto tabella. Vale per una sola istruzione.
with engine.connect() as conn:
    print("1. nome qualificato:", conn.execute(text("SELECT count(*) FROM cineteca.movies")).scalar())

# Secondo modo: SET search_path. Vale per la connection che lo esegue.
with engine.connect() as conn:
    conn.execute(text("SET search_path = cineteca, public"))
    print("2. SET search_path, nel blocco:", conn.execute(COUNT).scalar())

with engine.connect() as conn:
    try:
        conn.execute(COUNT)
    except Exception as error:
        print("2. SET search_path, in un altro blocco:", type(error.orig).__name__)

# Terzo modo: connect_args, valido per ogni connection di questo engine.
engine = create_engine(DATABASE_URL, connect_args={"options": "-c search_path=cineteca,public"})
for number in (1, 2):
    with engine.connect() as conn:
        print(f"3. connect_args, blocco {number}:", conn.execute(COUNT).scalar())
