"""Le regole sulle recensioni. Il film deve esistere: lo controlla la dependency del router."""
from sqlalchemy.orm import Session

from app.data import reviews as reviews_data
from app.models import Review
from app.schemas import ReviewCreate


def list_reviews(session: Session, movie_id: int) -> list[Review]:
    return reviews_data.list_reviews(session, movie_id)


def create_review(session: Session, movie_id: int, author: str, review: ReviewCreate) -> Review:
    created = reviews_data.create_review(session, movie_id, author, review.model_dump())
    session.commit()
    return created
