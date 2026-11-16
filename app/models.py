"""I model ORM della cineteca: una classe per ognuna delle sette tabelle dello schema cineteca."""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    MetaData,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    false,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    metadata = MetaData(schema="cineteca")


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (CheckConstraint("seats > 0", name="rooms_seats_check"),)

    room_id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    seats: Mapped[int]
    is_accessible: Mapped[bool] = mapped_column(server_default=false())


class Director(Base):
    __tablename__ = "directors"

    director_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    movies: Mapped[list["Movie"]] = relationship(back_populates="director", order_by="Movie.movie_id")


class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (UniqueConstraint("title", "release_year", name="movies_title_release_year_key"),)

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.director_id"))
    release_year: Mapped[int]
    runtime_min: Mapped[int]
    purchase_price_eur: Mapped[int]
    plot: Mapped[str | None] = mapped_column(Text)

    director: Mapped["Director"] = relationship(back_populates="movies")
    cast: Mapped[list["MovieActor"]] = relationship(
        back_populates="movie", order_by="MovieActor.actor_id", cascade="all, delete-orphan"
    )


class Actor(Base):
    __tablename__ = "actors"

    actor_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class MovieActor(Base):
    """Tabella ponte del molti a molti: la Primary Key sta su due colonne, e c'è una colonna sua."""

    __tablename__ = "movie_actors"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("actors.actor_id", ondelete="CASCADE"), primary_key=True)
    character_name: Mapped[str] = mapped_column(String(100))

    movie: Mapped["Movie"] = relationship(back_populates="cast")
    actor: Mapped["Actor"] = relationship()


class Screening(Base):
    __tablename__ = "screenings"

    screening_id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.movie_id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ticket_price_eur: Mapped[Decimal] = mapped_column(Numeric(5, 2))


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("rating BETWEEN 1 AND 5", name="reviews_rating_check"),)

    review_id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.movie_id", ondelete="CASCADE"))
    author: Mapped[str] = mapped_column(String(20))
    rating: Mapped[int]
    text: Mapped[str] = mapped_column(String(500))
    has_spoilers: Mapped[bool] = mapped_column(server_default=false())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
