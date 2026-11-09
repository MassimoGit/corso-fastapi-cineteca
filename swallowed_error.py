"""Un errore inghiottito dentro engine.begin(): la transaction resta abortita."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(
    os.getenv("DATABASE_URL"),
    connect_args={"options": "-c search_path=cineteca,public"},
)

with engine.begin() as conn:
    try:
        conn.execute(text("INSERT INTO rooms (code, name, seats) VALUES ('S1', 'Sala doppia', 10)"))
    except IntegrityError:
        print("codice già usato, vado avanti")
    conn.execute(text("SELECT count(*) FROM rooms"))
