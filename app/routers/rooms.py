"""Le routes delle sale."""
from fastapi import APIRouter

from app.dependencies import SessionDep
from app.schemas import RoomRead
from app.services import rooms as rooms_service

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("")
def list_rooms(session: SessionDep) -> list[RoomRead]:
    return rooms_service.list_rooms(session)


@router.get("/by-code/{code}", responses={404: {"description": "The room does not exist"}})
def get_room_by_code(code: str, session: SessionDep) -> RoomRead:
    return rooms_service.get_room_by_code(session, code)
