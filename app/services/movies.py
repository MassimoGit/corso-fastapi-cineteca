"""Le regole sui film. Non sa niente di HTTP: se qualcosa non va solleva un'eccezione del dominio."""
from sqlalchemy.orm import Session

from app.data import movies as movies_data
from app.errors import MovieNotFoundError
from app.models import Movie
from app.schemas import MovieCreate


def list_movies(
    session: Session, director_id: int | None, max_runtime: int | None, search: str | None, skip: int, limit: int
) -> list[Movie]:
    return movies_data.list_movies(session, director_id, max_runtime, search, skip, limit)


def get_movie(session: Session, movie_id: int) -> Movie:
    """Regola: il film deve esistere."""
    movie = movies_data.get_movie(session, movie_id)
    if movie is None:
        raise MovieNotFoundError(movie_id)
    return movie


def create_movie(session: Session, movie: MovieCreate) -> Movie:
    # Il titolo doppio e il regista che non esiste li rifiuta il database: lo dice MovieConflictError.
    created = movies_data.create_movie(session, movie.model_dump())
    session.commit()
    return created


def update_movie(session: Session, movie_id: int, changes: dict) -> Movie:
    movie = movies_data.update_movie(session, movie_id, changes)
    if movie is None:
        raise MovieNotFoundError(movie_id)
    session.commit()
    return movie


def delete_movie(session: Session, movie_id: int) -> None:
    if not movies_data.delete_movie(session, movie_id):
        raise MovieNotFoundError(movie_id)
    session.commit()


def list_catalogue(session: Session) -> list[tuple]:
    return movies_data.list_catalogue(session)


def list_cast(session: Session, movie_id: int) -> list[tuple]:
    get_movie(session, movie_id)  # regola: il film deve esistere, altrimenti MovieNotFoundError
    return movies_data.list_cast(session, movie_id)


def get_movie_detail(session: Session, movie_id: int) -> Movie:
    movie = movies_data.get_movie_detail(session, movie_id)
    if movie is None:
        raise MovieNotFoundError(movie_id)
    return movie
