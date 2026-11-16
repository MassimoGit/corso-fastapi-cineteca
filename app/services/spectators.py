"""Le regole sugli spettatori: il token lo decide il servizio, non chi si registra."""
import secrets

from sqlalchemy.orm import Session

from app.data import spectators as spectators_data
from app.models import Spectator


def create_spectator(session: Session, name: str) -> Spectator:
    # 32 byte casuali dal generatore sicuro del sistema operativo, scritti in 43 caratteri adatti a un header
    token = secrets.token_urlsafe(32)
    created = spectators_data.create_spectator(session, name, token)
    session.commit()
    return created


def find_spectator(session: Session, token: str) -> Spectator | None:
    return spectators_data.get_spectator_by_token(session, token)
