"""Registrazione, autenticazione e gestione utenti dello staff."""
from sqlalchemy.orm import Session

from app.data import users as users_data
from app.models import User
from app.security import DUMMY_HASH, hash_password, verify_and_update_password


def register_staff_user(session: Session, username: str, plain_password: str) -> User:
    """Registra un nuovo utente con ruolo staff: il ruolo non si accetta mai dal client."""
    hashed = hash_password(plain_password)
    created = users_data.create_user(session, username, hashed, role="staff")
    session.commit()
    return created


def authenticate_user(session: Session, username: str, plain_password: str) -> User | None:
    """Verifica username e password impiegando lo stesso tempo anche quando l'utente manca."""
    user = users_data.get_user_by_username(session, username)
    stored_hash = user.hashed_password if user is not None else DUMMY_HASH
    verified, new_hash = verify_and_update_password(plain_password, stored_hash)
    if user is None or not verified:
        return None
    if new_hash is not None:
        user.hashed_password = new_hash
        session.commit()
    return user


def get_user_by_username(session: Session, username: str) -> User | None:
    return users_data.get_user_by_username(session, username)


def list_users(session: Session) -> list[User]:
    return users_data.list_users(session)
