"""Errore comune: il router esiste ma nessuno lo include."""
from fastapi import FastAPI

from app.routers import movies, rooms  # noqa: F401  (rooms è importato ma mai incluso)

app = FastAPI()
app.include_router(movies.router)
# manca: app.include_router(rooms.router)
