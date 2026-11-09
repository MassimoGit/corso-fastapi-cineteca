"""Il livello dati delle recensioni."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Review


def list_reviews(session: Session, movie_id: int) -> list[Review]:
    query = select(Review).where(Review.movie_id == movie_id).order_by(Review.review_id)
    return session.scalars(query).all()


def create_review(session: Session, movie_id: int, author: str, values: dict) -> Review:
    review = Review(movie_id=movie_id, author=author, **values)
    session.add(review)
    session.flush()  # l'INSERT parte adesso: il database assegna review_id
    return review
