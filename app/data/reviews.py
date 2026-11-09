"""Il livello dati delle recensioni."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Review


def list_reviews(movie_id: int) -> list[Review]:
    query = select(Review).where(Review.movie_id == movie_id).order_by(Review.review_id)
    with Session(engine) as session:
        return session.scalars(query).all()


def create_review(movie_id: int, author: str, values: dict) -> Review:
    review = Review(movie_id=movie_id, author=author, **values)
    with Session(engine) as session:
        session.add(review)
        session.commit()
        session.refresh(review)
        return review
