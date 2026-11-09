"""Crea e popola lo schema cineteca eseguendo il file cineteca.sql."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))
sql_script = (BASE / "cineteca.sql").read_text(encoding="utf-8")

with engine.connect() as conn:
    conn.execute(text(sql_script))
    conn.commit()

    tables = conn.execute(text("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'cineteca'
        ORDER BY tablename
    """)).scalars().all()
    print("tabelle in cineteca:", tables)

    movies_count = conn.execute(text("SELECT count(*) FROM cineteca.movies")).scalar()
    rooms_count = conn.execute(text("SELECT count(*) FROM cineteca.rooms")).scalar()
    print(f"film caricati: {movies_count} - sale caricate: {rooms_count}")
