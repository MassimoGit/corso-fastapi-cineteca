"""Le regole sulle recensioni. Il film deve esistere: lo controlla la dependency del router."""
from app.data import reviews as reviews_data
from app.models import Review
from app.schemas import ReviewCreate


def list_reviews(movie_id: int) -> list[Review]:
    return reviews_data.list_reviews(movie_id)


def create_review(movie_id: int, author: str, review: ReviewCreate) -> Review:
    return reviews_data.create_review(movie_id, author, review.model_dump())
