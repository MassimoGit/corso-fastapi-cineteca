"""Il punto di ingresso: crea l'app, registra i gestori degli errori e include i router."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.database import engine, settings
from app.dependencies import SettingsDep, log_request
from app.errors import register_error_handlers
from app.routers import assistant, auth, catalogue, directors, movies, reports, reviews, rooms, spectators


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Il prima e il dopo della vita dell'app: tutto ciò che sta prima di yield gira all'avvio, il resto allo spegnimento."""
    yield
    engine.dispose()  # chiude le connessioni del pool


app = FastAPI(
    title=settings.app_name, version=settings.app_version, dependencies=[Depends(log_request)], lifespan=lifespan
)
register_error_handlers(app)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(movies.staff_router)
app.include_router(movies.admin_router)
app.include_router(directors.router)
app.include_router(directors.staff_router)
app.include_router(catalogue.router)
app.include_router(rooms.router)
app.include_router(reviews.router)
app.include_router(spectators.router)
app.include_router(reports.router)
app.include_router(assistant.router)


@app.get("/", tags=["info"])
def get_info(settings: SettingsDep) -> dict:
    return {"name": settings.app_name, "version": settings.app_version}
