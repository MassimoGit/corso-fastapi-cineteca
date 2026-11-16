"""Le dependency dell'app: funzioni che FastAPI esegue prima dell'endpoint che le dichiara."""
import secrets
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import Settings, engine, get_settings
from app.models import Movie
from app.services import movies as movies_service
from app.services import spectators as spectators_service

SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_session() -> Iterator[Session]:
    """Una Session per richiesta: la usano route, servizi e dati, e si chiude a richiesta finita."""
    # expire_on_commit=False: dopo il commit gli oggetti restano leggibili, senza una nuova SELECT
    with Session(engine, expire_on_commit=False) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def pagination(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> dict:
    """skip e limit delle liste."""
    return {"skip": skip, "limit": limit}


PageDep = Annotated[dict, Depends(pagination)]


def get_movie_or_404(movie_id: int, session: SessionDep) -> Movie:
    """Il film del path, oppure la risposta 404: il servizio solleva MovieNotFoundError e il gestore la traduce."""
    return movies_service.get_movie(session, movie_id)


MovieDep = Annotated[Movie, Depends(get_movie_or_404)]


# Un 401 deve dire come ci si autentica: WWW-Authenticate, con lo stesso nome che manda FastAPI per quello schema
API_KEY_CHALLENGE = {"WWW-Authenticate": "APIKey"}
BEARER_CHALLENGE = {"WWW-Authenticate": "Bearer"}

# Legge l'header X-API-Key e lo dichiara a /docs (il lucchetto). Header mancante: FastAPI risponde da solo 401.
# scheme_name: due schemi di sicurezza nella stessa app hanno bisogno di due nomi diversi.
api_key_header = APIKeyHeader(
    name="X-API-Key", scheme_name="AdminApiKey", description="Chiave di amministrazione della cineteca"
)
# Legge "Authorization: Bearer <token>": il token dello spettatore. Header mancante o schema diverso: 401 da solo.
bearer_scheme = HTTPBearer(scheme_name="SpectatorToken", description="Token della tessera dello spettatore")


def require_api_key(settings: SettingsDep, api_key: Annotated[str, Depends(api_key_header)]) -> None:
    """Lascia passare la richiesta solo se porta la chiave di amministrazione giusta."""
    expected = settings.admin_api_key.get_secret_value()
    # compare_digest: tempo di confronto che non dipende da dove le due chiavi cominciano a differire.
    # Vuole bytes: con str solleva TypeError appena trova un carattere non ASCII.
    if not secrets.compare_digest(api_key.encode(), expected.encode()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid API key", headers=API_KEY_CHALLENGE)


def get_spectator(
    session: SessionDep, credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]
) -> str:
    """Il nome dello spettatore a cui appartiene il token dell'header Authorization: Bearer."""
    spectator = spectators_service.find_spectator(session, credentials.credentials)
    if spectator is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid spectator token", headers=BEARER_CHALLENGE)
    return spectator.name


SpectatorDep = Annotated[str, Depends(get_spectator)]


def log_request(request: Request) -> None:
    """Dependency dell'intera app: scrive una riga per ogni richiesta che trova una route."""
    print(f"[request] {request.method} {request.url.path}")
