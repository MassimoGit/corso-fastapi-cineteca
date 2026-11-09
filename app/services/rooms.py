"""Le regole sulle sale."""
from app.data import rooms as rooms_data
from app.errors import RoomNotFoundError
from app.models import Room


def list_rooms() -> list[Room]:
    return rooms_data.list_rooms()


def get_room_by_code(code: str) -> Room:
    room = rooms_data.get_room_by_code(code)
    if room is None:
        raise RoomNotFoundError(code)
    return room
