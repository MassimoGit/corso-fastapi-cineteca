"""Il search_path di una connessione Python è lo stesso di DBeaver."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    print("search_path:", conn.execute(text("SHOW search_path")).scalar())
    print("utente e database:", conn.execute(text("SELECT current_user, current_database()")).first())
    print("clienti, senza schema:", conn.execute(text("SELECT count(*) FROM clienti")).scalar())
