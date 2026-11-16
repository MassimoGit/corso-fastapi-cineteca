"""Le routes degli spettatori: le registra solo l'amministrazione."""
from fastapi import APIRouter, Depends, status

from app.dependencies import SessionDep, require_api_key
from app.schemas import SpectatorCard, SpectatorCreate
from app.services import spectators as spectators_service

router = APIRouter(
    prefix="/spectators",
    tags=["spectators"],
    dependencies=[Depends(require_api_key)],
    responses={401: {"description": "Missing or invalid API key"}},
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "A spectator with this name already exists"}},
)
def create_spectator(spectator: SpectatorCreate, session: SessionDep) -> SpectatorCard:
    return spectators_service.create_spectator(session, spectator.name)
