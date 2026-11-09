"""Le routes delle sale."""
from fastapi import APIRouter

from app.schemas import RoomRead
from app.services import rooms as rooms_service

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("")
def list_rooms() -> list[RoomRead]:
    return rooms_service.list_rooms()


@router.get("/by-code/{code}", responses={404: {"description": "The room does not exist"}})
def get_room_by_code(code: str) -> RoomRead:
    return rooms_service.get_room_by_code(code)
