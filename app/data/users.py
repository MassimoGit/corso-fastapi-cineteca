"""Il livello dati degli utenti dello staff."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors import UserConflictError
from app.models import User


def create_user(session: Session, username: str, hashed_password: str, role: str = "staff") -> User:
    user = User(username=username, hashed_password=hashed_password, role=role)
    session.add(user)
    try:
        session.flush()
    except IntegrityError:
        raise UserConflictError(username)
    return user


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.scalars(select(User).where(User.username == username)).first()


def list_users(session: Session) -> list[User]:
    return list(session.scalars(select(User).order_by(User.user_id)).all())
