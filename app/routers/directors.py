"""Le routes dei registi."""
from fastapi import APIRouter, Depends, status

from app.dependencies import SessionDep, require_api_key
from app.schemas import DirectorCreate, DirectorRead
from app.services import directors as directors_service

router = APIRouter(prefix="/directors", tags=["directors"])

admin_router = APIRouter(
    prefix="/directors",
    tags=["directors"],
    dependencies=[Depends(require_api_key)],
    responses={401: {"description": "Missing or invalid API key"}},
)


@router.get("")
def list_directors(session: SessionDep) -> list[DirectorRead]:
    return directors_service.list_directors(session)


@admin_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "A director with this name already exists"}},
)
def create_director(director: DirectorCreate, session: SessionDep) -> DirectorRead:
    return directors_service.create_director(session, director.name)
