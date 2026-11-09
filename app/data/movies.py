"""Il livello dati dei film: l'unico che parla con il database. Ogni funzione apre la sua Session."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import engine
from app.errors import MovieConflictError
from app.models import Movie


def list_movies(
    director_id: int | None, max_runtime: int | None, search: str | None, skip: int, limit: int
) -> list[Movie]:
    query = select(Movie).order_by(Movie.movie_id)
    if director_id is not None:
        query = query.where(Movie.director_id == director_id)
    if max_runtime is not None:
        query = query.where(Movie.runtime_min <= max_runtime)
    if search is not None:
        query = query.where(Movie.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit)
    with Session(engine) as session:
        return session.scalars(query).all()


def get_movie(movie_id: int) -> Movie | None:
    """Il film con questo id, oppure None: cosa farne lo decide il servizio."""
    with Session(engine) as session:
        return session.get(Movie, movie_id)


def create_movie(values: dict) -> Movie:
    movie = Movie(**values)
    with Session(engine) as session:
        session.add(movie)
        _commit(session)
        session.refresh(movie)
        return movie


def update_movie(movie_id: int, changes: dict) -> Movie | None:
    """Applica i campi cambiati. Restituisce None se il film non esiste."""
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)
        if movie is None:
            return None
        for name, value in changes.items():
            setattr(movie, name, value)
        _commit(session)
        session.refresh(movie)
        return movie


def delete_movie(movie_id: int) -> bool:
    """False se il film non esiste."""
    with Session(engine) as session:
        movie = session.get(Movie, movie_id)
        if movie is None:
            return False
        session.delete(movie)
        session.commit()
        return True


def _commit(session: Session) -> None:
    """Il commit con il vincolo del database tradotto in un'eccezione del dominio."""
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise MovieConflictError()
