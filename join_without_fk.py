"""Senza ForeignKey nel model, SQLAlchemy non sa come collegare due classi: join(Director) non funziona."""
from sqlalchemy import MetaData, String, select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.database import engine


class OldBase(DeclarativeBase):
    metadata = MetaData(schema="cineteca")


class Director(OldBase):
    __tablename__ = "directors"

    director_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class Movie(OldBase):
    """Il Movie della lezione precedente: director_id è un intero qualsiasi, nessuna ForeignKey."""

    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    director_id: Mapped[int]


with Session(engine) as session:
    try:
        session.execute(select(Movie.title, Director.name).join(Director)).all()
    except InvalidRequestError as error:
        print(type(error).__name__)
        print(error)

    # La condizione scritta a mano funziona anche senza ForeignKey.
    rows = session.execute(
        select(Movie.title, Director.name).join(Director, Movie.director_id == Director.director_id).limit(2)
    ).all()
    print("con la condizione esplicita:", [tuple(row) for row in rows])
