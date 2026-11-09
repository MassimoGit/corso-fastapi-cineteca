"""Caricare le relationship insieme alla query principale: selectinload per le liste, joinedload per un singolo oggetto."""
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.database import engine
from app.models import Director, Movie

with Session(engine) as session:
    query = select(Director).options(selectinload(Director.movies)).order_by(Director.director_id)
    directors = session.scalars(query).all()
    print("registi caricati:", len(directors))
    for director in directors:
        print(f"{director.name}: {len(director.movies)} film")

    print()
    query = select(Movie).options(joinedload(Movie.director)).order_by(Movie.movie_id)
    movies = session.scalars(query).all()
    print("film caricati:", len(movies))
    for movie in movies[:2]:
        print(f"{movie.title}: {movie.director.name}")
