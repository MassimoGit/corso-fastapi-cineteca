"""Errore comune: la recensione viene scritta ma nessuno fa il commit."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.data import reviews as reviews_data
from app.dependencies import SessionDep
from app.schemas import ReviewCreate, ReviewRead
from app.services import reviews as reviews_service

app = FastAPI()


def create_review(session: Session, movie_id: int, author: str, review: ReviewCreate):
    return reviews_data.create_review(session, movie_id, author, review.model_dump())
    # SBAGLIATO: manca session.commit()


@app.post("/movies/{movie_id}/reviews", status_code=201)
def post_review(movie_id: int, review: ReviewCreate, session: SessionDep) -> ReviewRead:
    return create_review(session, movie_id, "luca_77", review)


@app.get("/movies/{movie_id}/reviews")
def get_reviews(movie_id: int, session: SessionDep) -> list[ReviewRead]:
    return reviews_service.list_reviews(session, movie_id)


if __name__ == "__main__":
    client = TestClient(app)
    body = {"rating": 4, "text": "Bello, lo rivedrei volentieri.", "has_spoilers": False}
    response = client.post("/movies/1/reviews", json=body)
    print("POST /movies/1/reviews ->", response.status_code, response.json())
    response = client.get("/movies/1/reviews")
    print("GET /movies/1/reviews ->", response.status_code, "- review_id:", [r["review_id"] for r in response.json()])
