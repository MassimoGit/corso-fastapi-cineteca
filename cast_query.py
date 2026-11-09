"""Il cast di un film: un join a tre tabelle, con il personaggio che sta nella tabella ponte."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Actor, Movie, MovieActor

query = (
    select(Movie.title, Actor.name, MovieActor.character_name)
    .join(MovieActor, MovieActor.movie_id == Movie.movie_id)
    .join(Actor, Actor.actor_id == MovieActor.actor_id)
    .where(Movie.movie_id == 3)
    .order_by(Actor.name)
)

print(query)
print()

with Session(engine) as session:
    for row in session.execute(query):
        print(f"{row.title}: {row.name} è {row.character_name}")
