"""Senza il nome dello schema, la tabella rooms non si trova."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    print(conn.execute(text("SELECT count(*) FROM rooms")).scalar())
