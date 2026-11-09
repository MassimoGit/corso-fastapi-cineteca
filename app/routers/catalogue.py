"""Le routes che leggono dati di più tabelle: il catalogo con i registi e i conteggi."""
from fastapi import APIRouter

from app.dependencies import SessionDep
from app.schemas import CatalogueRow, DirectorStats
from app.services import directors as directors_service
from app.services import movies as movies_service

router = APIRouter(tags=["catalogue"])


@router.get("/catalogue")
def list_catalogue(session: SessionDep) -> list[CatalogueRow]:
    return movies_service.list_catalogue(session)


@router.get("/stats/movies-per-director")
def movies_per_director(session: SessionDep) -> list[DirectorStats]:
    return directors_service.movies_per_director(session)
