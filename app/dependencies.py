"""Le dependency dell'app: funzioni che FastAPI esegue prima dell'endpoint che le dichiara."""
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Query, Request, status

from app.database import Settings, get_settings
from app.models import Movie
from app.services import movies as movies_service

SettingsDep = Annotated[Settings, Depends(get_settings)]


def pagination(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict:
    """skip e limit delle liste."""
    return {"skip": skip, "limit": limit}


PageDep = Annotated[dict, Depends(pagination)]


def get_movie_or_404(movie_id: int) -> Movie:
    """Il film del path, oppure la risposta 404: il servizio solleva MovieNotFoundError e il gestore la traduce."""
    return movies_service.get_movie(movie_id)


MovieDep = Annotated[Movie, Depends(get_movie_or_404)]


def get_spectator(settings: SettingsDep, x_spectator: Annotated[str, Header()]) -> str:
    """Lo spettatore che manda la richiesta, letto dall'header X-Spectator."""
    if x_spectator not in settings.spectators:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unknown spectator {x_spectator}")
    return x_spectator


SpectatorDep = Annotated[str, Depends(get_spectator)]


def log_request(request: Request) -> None:
    """Dependency dell'intera app: scrive una riga per ogni richiesta che trova una route."""
    print(f"[request] {request.method} {request.url.path}")
