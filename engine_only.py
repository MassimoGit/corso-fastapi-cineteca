"""create_engine prepara tutto ma non si collega: nessuna rete, nessun errore."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))
print("engine creato:", engine)
print("driver in uso:", engine.dialect.driver)
