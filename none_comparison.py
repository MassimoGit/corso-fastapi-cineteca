"""Cercare i film senza trama: is_(None) funziona, "is None" di Python no."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Movie

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

with Session(engine) as session:
    wrong = select(Movie).where(Movie.plot is None)  # SBAGLIATO: "is" è un operatore di Python
    print("SQL di where(Movie.plot is None):")
    print(wrong)
    print("film trovati:", len(session.scalars(wrong).all()))

    right = select(Movie).where(Movie.plot.is_(None))
    print("SQL di where(Movie.plot.is_(None)):")
    print(right)
    print("film trovati:", len(session.scalars(right).all()))
