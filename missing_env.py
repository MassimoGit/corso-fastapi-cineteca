"""Il .env non viene trovato: DATABASE_URL è None e create_engine protesta."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE = Path(__file__).resolve().parent
found = load_dotenv(BASE / "env.txt")  # il file si chiama .env, non env.txt
print("file caricato:", found)

url = os.getenv("DATABASE_URL")
print("DATABASE_URL:", url)

engine = create_engine(url)
