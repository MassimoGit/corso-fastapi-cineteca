"""Le routes di autenticazione: registrazione staff, login su /token e profilo corrente."""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import BEARER_CHALLENGE, CurrentUserDep, SessionDep, SettingsDep, require_admin
from app.schemas import Token, UserCreate, UserRead
from app.security import create_access_token
from app.services import auth as auth_service

router = APIRouter(tags=["auth"])


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Username already registered"}},
)
def register_user(user: UserCreate, session: SessionDep) -> UserRead:
    """Registra un nuovo membro dello staff salvando solo l'hash argon2id della password."""
    return auth_service.register_staff_user(session, user.username, user.password.get_secret_value())


@router.post(
    "/token",
    responses={401: {"description": "Invalid username or password"}},
)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
    settings: SettingsDep,
) -> Token:
    """Riceve username e password come form data e restituisce un access token JWT Bearer."""
    user = auth_service.authenticate_user(session, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
            headers=BEARER_CHALLENGE,
        )
    token = create_access_token(
        subject=user.username,
        role=user.role,
        secret_key=settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
        expires_delta=timedelta(minutes=settings.jwt_expire_minutes),
    )
    return Token(access_token=token)


@router.get("/users/me")
def read_current_user(current_user: CurrentUserDep) -> UserRead:
    """Restituisce l'utente associato al JWT inviato nell'header Authorization."""
    return current_user


@router.get(
    "/users",
    dependencies=[Depends(require_admin)],
    responses={401: {"description": "Missing or invalid bearer token"}, 403: {"description": "Admin role required"}},
)
def list_users(session: SessionDep) -> list[UserRead]:
    """Elenco degli utenti registrati: riservato al ruolo admin."""
    return auth_service.list_users(session)
