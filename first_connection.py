"""La prima connessione: create_engine non si collega a niente, connect sì."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))
print("engine creato:", engine)

with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    print("server:", version)
