"""Il livello dati degli spettatori."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors import SpectatorConflictError
from app.models import Spectator


def create_spectator(session: Session, name: str, token: str) -> Spectator:
    spectator = Spectator(name=name, token=token)
    session.add(spectator)
    try:
        session.flush()
    except IntegrityError:
        raise SpectatorConflictError(name)
    return spectator


def get_spectator_by_token(session: Session, token: str) -> Spectator | None:
    return session.scalars(select(Spectator).where(Spectator.token == token)).first()
