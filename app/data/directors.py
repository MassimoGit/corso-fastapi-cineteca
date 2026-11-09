"""Il livello dati dei registi."""
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors import DirectorConflictError
from app.models import Director, Movie


def list_directors(session: Session) -> list[Director]:
    return session.scalars(select(Director).order_by(Director.director_id)).all()


def create_director(session: Session, name: str) -> Director:
    director = Director(name=name)
    session.add(director)
    try:
        session.flush()
    except IntegrityError:
        raise DirectorConflictError(name)
    return director


def movies_per_director(session: Session) -> list[tuple[str, int]]:
    """Quanti film ha ogni regista, anche zero: join esterno e count di una colonna della tabella di destra."""
    query = (
        select(Director.name.label("director"), func.count(Movie.movie_id).label("movies"))
        .join(Movie, isouter=True)
        .group_by(Director.name)
        .order_by(func.count(Movie.movie_id).desc(), Director.name)
    )
    return session.execute(query).all()
