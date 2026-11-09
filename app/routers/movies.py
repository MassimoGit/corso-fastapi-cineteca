"""Le routes dei film."""
from fastapi import APIRouter, status

from app.dependencies import MovieDep, PageDep
from app.schemas import MovieCreate, MovieRead, MovieUpdate
from app.services import movies as movies_service

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("")
def list_movies(
    page: PageDep,
    director_id: int | None = None,
    max_runtime: int | None = None,
    search: str | None = None,
) -> list[MovieRead]:
    return movies_service.list_movies(director_id, max_runtime, search, page["skip"], page["limit"])


@router.get("/{movie_id}", responses={404: {"description": "The movie does not exist"}})
def get_movie(movie: MovieDep) -> MovieRead:
    return movie


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Movie already in the catalogue or director_id not found"}},
)
def create_movie(movie: MovieCreate) -> MovieRead:
    return movies_service.create_movie(movie)


@router.patch(
    "/{movie_id}",
    responses={
        404: {"description": "The movie does not exist"},
        409: {"description": "Movie already in the catalogue or director_id not found"},
    },
)
def update_movie(movie_id: int, changes: MovieUpdate) -> MovieRead:
    return movies_service.update_movie(movie_id, changes.model_dump(exclude_unset=True))


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "The movie does not exist"}},
)
def delete_movie(movie_id: int) -> None:
    movies_service.delete_movie(movie_id)
