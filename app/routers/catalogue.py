"""Le routes che leggono dati di più tabelle: il catalogo pubblico e le statistiche riservate all'admin."""
from fastapi import APIRouter, Depends

from app.dependencies import SessionDep, require_admin
from app.schemas import CatalogueRow, DirectorStats
from app.services import directors as directors_service
from app.services import movies as movies_service

router = APIRouter(tags=["catalogue"])


@router.get("/catalogue")
def list_catalogue(session: SessionDep) -> list[CatalogueRow]:
    return movies_service.list_catalogue(session)


@router.get(
    "/stats/movies-per-director",
    dependencies=[Depends(require_admin)],
    responses={401: {"description": "Missing or invalid bearer token"}, 403: {"description": "Admin role required"}},
)
def movies_per_director(session: SessionDep) -> list[DirectorStats]:
    return directors_service.movies_per_director(session)
