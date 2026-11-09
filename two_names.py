"""Errore comune: due colonne che si chiamano name nello stesso select, senza label."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Actor, Director, Movie, MovieActor

query = (
    select(Director.name, Actor.name)  # SBAGLIATO: due colonne `name`, nessuna label
    .select_from(Movie)
    .join(Director, Director.director_id == Movie.director_id)
    .join(MovieActor, MovieActor.movie_id == Movie.movie_id)
    .join(Actor, Actor.actor_id == MovieActor.actor_id)
    .where(Movie.movie_id == 3)
    .order_by(Actor.name)
)

with Session(engine) as session:
    row = session.execute(query).first()
    print("riga:", tuple(row))
    print("row.name:", row.name)
