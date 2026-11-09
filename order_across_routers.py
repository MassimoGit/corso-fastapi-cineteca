"""Errore comune: l'ordine delle routes vale anche fra router diversi."""
from fastapi import APIRouter, FastAPI

movies_router = APIRouter(prefix="/movies", tags=["movies"])
featured_router = APIRouter(prefix="/movies", tags=["featured"])


@movies_router.get("/{movie_id}")
def get_movie(movie_id: int) -> dict:
    return {"movie_id": movie_id}


@featured_router.get("/featured")
def get_featured() -> dict:
    return {"featured": "Inception"}


app = FastAPI()
app.include_router(movies_router)
app.include_router(featured_router)  # incluso dopo: /movies/{movie_id} vince
