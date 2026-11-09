"""Il livello dati dei film: l'unico che parla con il database. Riceve la Session, non la apre e non fa commit."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors import MovieConflictError
from app.models import Movie


def list_movies(
    session: Session, director_id: int | None, max_runtime: int | None, search: str | None, skip: int, limit: int
) -> list[Movie]:
    query = select(Movie).order_by(Movie.movie_id)
    if director_id is not None:
        query = query.where(Movie.director_id == director_id)
    if max_runtime is not None:
        query = query.where(Movie.runtime_min <= max_runtime)
    if search is not None:
        query = query.where(Movie.title.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit)
    return session.scalars(query).all()


def get_movie(session: Session, movie_id: int) -> Movie | None:
    """Il film con questo id, oppure None: cosa farne lo decide il servizio."""
    return session.get(Movie, movie_id)


def create_movie(session: Session, values: dict) -> Movie:
    movie = Movie(**values)
    session.add(movie)
    _flush(session)
    return movie


def update_movie(session: Session, movie_id: int, changes: dict) -> Movie | None:
    """Applica i campi cambiati. Restituisce None se il film non esiste."""
    movie = session.get(Movie, movie_id)
    if movie is None:
        return None
    for name, value in changes.items():
        setattr(movie, name, value)
    _flush(session)
    return movie


def delete_movie(session: Session, movie_id: int) -> bool:
    """False se il film non esiste."""
    movie = session.get(Movie, movie_id)
    if movie is None:
        return False
    session.delete(movie)
    return True


def _flush(session: Session) -> None:
    """Manda le modifiche al database: un vincolo violato diventa un'eccezione del dominio."""
    try:
        session.flush()
    except IntegrityError:
        raise MovieConflictError()
