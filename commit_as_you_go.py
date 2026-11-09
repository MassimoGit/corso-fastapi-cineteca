"""conn.commit(): la modifica diventa definitiva (lo stile "commit as you go")."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
SEATS = text("SELECT seats FROM cineteca.rooms WHERE code = 'S1'")

with engine.connect() as conn:
    conn.execute(text("UPDATE cineteca.rooms SET seats = 130 WHERE code = 'S1'"))
    conn.commit()
    print("dopo il commit, posti della sala S1:", conn.execute(SEATS).scalar())

with engine.connect() as conn:
    print("in una nuova connection, posti della sala S1:", conn.execute(SEATS).scalar())

    # Rimettiamo i posti com'erano, con un altro commit.
    conn.execute(text("UPDATE cineteca.rooms SET seats = 120 WHERE code = 'S1'"))
    conn.commit()
