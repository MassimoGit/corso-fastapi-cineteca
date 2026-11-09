"""Il punto di ingresso: crea l'app, registra i gestori degli errori e include i router."""
from fastapi import Depends, FastAPI

from app.database import settings
from app.dependencies import SettingsDep, log_request
from app.errors import register_error_handlers
from app.routers import catalogue, directors, movies, reviews, rooms

app = FastAPI(title=settings.app_name, version=settings.app_version, dependencies=[Depends(log_request)])
register_error_handlers(app)

app.include_router(movies.router)
app.include_router(directors.router)
app.include_router(catalogue.router)
app.include_router(rooms.router)
app.include_router(reviews.router)


@app.get("/", tags=["info"])
def get_info(settings: SettingsDep) -> dict:
    return {"name": settings.app_name, "version": settings.app_version}
