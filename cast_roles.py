"""Il cast attraverso la tabella ponte: Movie.cast -> MovieActor -> Actor."""
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Movie

with Session(engine) as session:
    movie = session.get(Movie, 3)
    for role in movie.cast:
        print(f"{role.actor.name} è {role.character_name}")
