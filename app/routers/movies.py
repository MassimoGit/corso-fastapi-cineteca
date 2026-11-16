"""Le routes dei film."""
from fastapi import APIRouter, Depends, status

from app.dependencies import MovieDep, PageDep, SessionDep, require_api_key
from app.schemas import CastMember, MovieCreate, MovieDetail, MovieRead, MovieUpdate
from app.services import movies as movies_service

# Le letture sono libere
router = APIRouter(prefix="/movies", tags=["movies"])

# Le scritture vogliono la chiave: la dependency del router vale per ogni route che si aggiunge qui sotto
admin_router = APIRouter(
    prefix="/movies",
    tags=["movies"],
    dependencies=[Depends(require_api_key)],
    responses={401: {"description": "Missing or invalid API key"}},
)


@router.get("")
def list_movies(
    session: SessionDep,
    page: PageDep,
    director_id: int | None = None,
    max_runtime: int | None = None,
    search: str | None = None,
) -> list[MovieRead]:
    return movies_service.list_movies(session, director_id, max_runtime, search, page["skip"], page["limit"])


@router.get("/{movie_id}", responses={404: {"description": "The movie does not exist"}})
def get_movie(movie: MovieDep) -> MovieRead:
    return movie


@router.get("/{movie_id}/detail", responses={404: {"description": "The movie does not exist"}})
def get_movie_detail(movie_id: int, session: SessionDep) -> MovieDetail:
    return movies_service.get_movie_detail(session, movie_id)


@router.get("/{movie_id}/cast", responses={404: {"description": "The movie does not exist"}})
def list_cast(movie_id: int, session: SessionDep) -> list[CastMember]:
    return movies_service.list_cast(session, movie_id)


@admin_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Movie already in the catalogue or director_id not found"}},
)
def create_movie(movie: MovieCreate, session: SessionDep) -> MovieRead:
    return movies_service.create_movie(session, movie)


@admin_router.patch(
    "/{movie_id}",
    responses={
        404: {"description": "The movie does not exist"},
        409: {"description": "Movie already in the catalogue or director_id not found"},
    },
)
def update_movie(movie_id: int, changes: MovieUpdate, session: SessionDep) -> MovieRead:
    return movies_service.update_movie(session, movie_id, changes.model_dump(exclude_unset=True))


@admin_router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "The movie does not exist"}},
)
def delete_movie(movie_id: int, session: SessionDep) -> None:
    movies_service.delete_movie(session, movie_id)
