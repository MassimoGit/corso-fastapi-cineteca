"""Il pool: l'engine tiene aperte le connections e le riusa."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))
print("all'inizio:", engine.pool.status())

with engine.connect() as conn:
    first_pid = conn.execute(text("SELECT pg_backend_pid()")).scalar()
    print("dentro il primo blocco:", engine.pool.status())

print("dopo il primo blocco:", engine.pool.status())

with engine.connect() as conn:
    second_pid = conn.execute(text("SELECT pg_backend_pid()")).scalar()

print("stesso processo sul server:", first_pid == second_pid)
