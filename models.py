"""I model ORM di Room e Movie nello schema cineteca."""
from sqlalchemy import MetaData, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(schema="cineteca")


class Room(Base):
    __tablename__ = "rooms"

    room_id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(50))
    seats: Mapped[int]


class Movie(Base):
    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    director_id: Mapped[int]
    release_year: Mapped[int]
    runtime_min: Mapped[int]
    purchase_price_eur: Mapped[int]
    plot: Mapped[str | None] = mapped_column(Text)
