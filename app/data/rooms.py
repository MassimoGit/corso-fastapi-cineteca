"""Il livello dati delle sale."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Room


def list_rooms(session: Session) -> list[Room]:
    return session.scalars(select(Room).order_by(Room.room_id)).all()


def get_room_by_code(session: Session, code: str) -> Room | None:
    return session.scalars(select(Room).where(Room.code == code)).one_or_none()
