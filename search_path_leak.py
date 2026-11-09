"""SET search_path: senza commit sparisce, con il commit resta sulla connection che il pool riusa."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
SHOW = text("SHOW search_path")
SET = text("SET search_path = cineteca, public")

engine = create_engine(DATABASE_URL)

# Senza commit: alla chiusura del blocco c'è il ROLLBACK, e il SET è transazionale come tutto il resto.
with engine.connect() as conn:
    conn.execute(SET)
    print("SET senza commit, dentro il blocco:", conn.execute(SHOW).scalar())
with engine.connect() as conn:
    print("SET senza commit, nuovo blocco:", conn.execute(SHOW).scalar())

# Con il commit: la connection torna al pool, e il pool la riusa con il SET ancora attivo.
with engine.connect() as conn:
    conn.execute(SET)
    conn.commit()
    print("SET con commit, dentro il blocco:", conn.execute(SHOW).scalar())
with engine.connect() as conn:
    print("SET con commit, nuovo blocco:", conn.execute(SHOW).scalar())
engine.dispose()

# Un engine nuovo ha un pool nuovo, e riparte dal search_path del ruolo.
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    print("engine nuovo:", conn.execute(SHOW).scalar())
engine.dispose()
