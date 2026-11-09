"""Le regole sulle sale."""
from sqlalchemy.orm import Session

from app.data import rooms as rooms_data
from app.errors import RoomNotFoundError
from app.models import Room


def list_rooms(session: Session) -> list[Room]:
    return rooms_data.list_rooms(session)


def get_room_by_code(session: Session, code: str) -> Room:
    room = rooms_data.get_room_by_code(session, code)
    if room is None:
        raise RoomNotFoundError(code)
    return room
