"""Il livello dati delle sale."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Room


def list_rooms() -> list[Room]:
    with Session(engine) as session:
        return session.scalars(select(Room).order_by(Room.room_id)).all()


def get_room_by_code(code: str) -> Room | None:
    with Session(engine) as session:
        return session.scalars(select(Room).where(Room.code == code)).one_or_none()
