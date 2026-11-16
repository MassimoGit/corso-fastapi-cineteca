"""Le dependency dell'app: funzioni che FastAPI esegue prima della route che le dichiara."""
import secrets
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.database import Settings, engine, get_settings
from app.models import Movie, User
from app.security import decode_access_token
from app.services import auth as auth_service
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

# Tre schemi di sicurezza con scheme_name diversi per non sovrapporsi in OpenAPI (/docs):
# - AdminApiKey: chiave condivisa di servizio (es. registrazione spettatori)
# - SpectatorToken: tessera opaca degli spettatori per le recensioni
# - StaffAuth: login username/password su POST /token con risposta JWT Bearer per lo staff
api_key_header = APIKeyHeader(
    name="X-API-Key", scheme_name="AdminApiKey", description="Chiave di servizio per la registrazione spettatori"
)
bearer_scheme = HTTPBearer(scheme_name="SpectatorToken", description="Token della tessera dello spettatore")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", scheme_name="StaffAuth", description="Account dello staff con username e password"
)


def require_api_key(settings: SettingsDep, api_key: Annotated[str, Depends(api_key_header)]) -> None:
    """Lascia passare la richiesta solo se porta la chiave di servizio giusta."""
    expected = settings.admin_api_key.get_secret_value()
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


def get_current_user(
    session: SessionDep, settings: SettingsDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """Decodifica il JWT Bearer, controlla firma e scadenza e carica l'utente dal database."""
    credentials_error = HTTPException(
        status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers=BEARER_CHALLENGE
    )
    try:
        payload = decode_access_token(token, settings.jwt_secret_key.get_secret_value(), settings.jwt_algorithm)
    except InvalidTokenError:
        raise credentials_error
    username = payload.get("sub")
    if not isinstance(username, str) or not username:
        raise credentials_error
    user = auth_service.get_user_by_username(session, username)
    if user is None:
        raise credentials_error
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def require_admin(current_user: CurrentUserDep) -> User:
    """Lascia passare solo gli utenti con ruolo admin; per gli altri risponde 403 Forbidden."""
    if current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="admin role required")
    return current_user


AdminDep = Annotated[User, Depends(require_admin)]


def log_request(request: Request) -> None:
    """Dependency dell'intera app: scrive una riga per ogni richiesta che trova una route."""
    print(f"[request] {request.method} {request.url.path}")
