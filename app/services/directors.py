"""Le regole sui registi."""
from sqlalchemy.orm import Session

from app.data import directors as directors_data
from app.models import Director


def list_directors(session: Session) -> list[Director]:
    return directors_data.list_directors(session)


def create_director(session: Session, name: str) -> Director:
    created = directors_data.create_director(session, name)
    session.commit()
    return created


def movies_per_director(session: Session) -> list[tuple[str, int]]:
    return directors_data.movies_per_director(session)
