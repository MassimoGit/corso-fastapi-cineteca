"""Il livello dati dei film: l'unico che parla con il database. Riceve la Session, non la apre e non fa commit."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, selectinload

from app.errors import MovieConflictError
from app.models import Actor, Director, Movie, MovieActor


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


def list_catalogue(session: Session) -> list[tuple]:
    """I film con il nome del regista: righe di colonne di due tabelle, non oggetti Movie."""
    query = (
        select(Movie.movie_id, Movie.title, Movie.release_year, Director.name.label("director_name"))
        .join(Director)
        .order_by(Movie.movie_id)
    )
    return session.execute(query).all()


def list_cast(session: Session, movie_id: int) -> list[tuple]:
    """Gli attori di un film con il personaggio, che sta nella tabella ponte."""
    query = (
        select(Actor.name.label("actor"), MovieActor.character_name.label("character"))
        .join(MovieActor, MovieActor.actor_id == Actor.actor_id)
        .where(MovieActor.movie_id == movie_id)
        .order_by(Actor.name)
    )
    return session.execute(query).all()


def get_movie_detail(session: Session, movie_id: int) -> Movie | None:
    """Il film con regista e cast già caricati: 3 query in tutto, qualunque sia il numero di attori."""
    query = (
        select(Movie)
        .where(Movie.movie_id == movie_id)
        .options(joinedload(Movie.director), selectinload(Movie.cast).selectinload(MovieActor.actor))
    )
    return session.scalars(query).one_or_none()
