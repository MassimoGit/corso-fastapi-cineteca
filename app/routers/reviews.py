"""Le routes delle recensioni di un film."""
from fastapi import APIRouter, Depends, status

from app.dependencies import SessionDep, SpectatorDep, get_movie_or_404
from app.schemas import ReviewCreate, ReviewRead
from app.services import reviews as reviews_service

# La dependency del router vale per tutte le routes: nessuna recensione per un film che non c'è.
router = APIRouter(
    prefix="/movies/{movie_id}/reviews",
    tags=["reviews"],
    dependencies=[Depends(get_movie_or_404)],
)


@router.get("")
def list_reviews(movie_id: int, session: SessionDep) -> list[ReviewRead]:
    return reviews_service.list_reviews(session, movie_id)


@router.post("", status_code=status.HTTP_201_CREATED, responses={401: {"description": "Unknown spectator"}})
def create_review(movie_id: int, review: ReviewCreate, spectator: SpectatorDep, session: SessionDep) -> ReviewRead:
    return reviews_service.create_review(session, movie_id, spectator, review)
