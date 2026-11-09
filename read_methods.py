"""Un oggetto o una lista: che cosa restituisce ogni metodo di lettura della Session."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session

from models import Movie

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

long_movies = select(Movie).where(Movie.runtime_min > 150).order_by(Movie.movie_id)
inception = select(Movie).where(Movie.title == "Inception")
titanic = select(Movie).where(Movie.title == "Titanic")

with Session(engine) as session:
    movie = session.get(Movie, 1)
    print("get(1):", type(movie).__name__, "-", movie.title)
    print("get(99):", session.get(Movie, 99))

    movies = session.scalars(long_movies).all()
    print("all():", type(movies).__name__, "di", len(movies), "oggetti")
    print("all(), nessun risultato:", session.scalars(titanic).all())

    print("first():", session.scalars(long_movies).first().title)
    print("first(), nessun risultato:", session.scalars(titanic).first())

    print("one_or_none():", session.scalars(inception).one_or_none().title)
    print("one_or_none(), nessun risultato:", session.scalars(titanic).one_or_none())
    try:
        session.scalars(long_movies).one_or_none()
    except MultipleResultsFound as error:
        print("one_or_none(), due risultati:", type(error).__name__)

    print("one():", session.scalars(inception).one().title)
    try:
        session.scalars(titanic).one()
    except NoResultFound as error:
        print("one(), nessun risultato:", type(error).__name__)

    rows = session.execute(long_movies).all()
    print("execute().all():", type(rows[0]).__name__, "con", len(rows[0]), "elemento ->", rows[0][0].title)
