"""Un errore dopo l'INSERT e prima del commit: alla chiusura della Session la transaction viene annullata."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.data import reviews as reviews_data
from app.database import settings
from app.dependencies import SessionDep
from app.errors import register_error_handlers
from app.models import Review
from app.schemas import ReviewCreate, ReviewRead

app = FastAPI()
register_error_handlers(app)


def send_notification(review: Review) -> None:
    """Avvisa il gestore della cineteca: qui il server di posta non risponde."""
    raise ConnectionError("mail server not reachable")


def create_review(session: Session, movie_id: int, author: str, review: ReviewCreate) -> Review:
    created = reviews_data.create_review(session, movie_id, author, review.model_dump())
    send_notification(created)  # fallisce dopo l'INSERT e prima del commit
    session.commit()
    return created


@app.post("/movies/{movie_id}/reviews", status_code=201)
def post_review(movie_id: int, review: ReviewCreate, session: SessionDep) -> ReviewRead:
    return create_review(session, movie_id, "luca_77", review)


def count_reviews() -> int:
    """Conta le recensioni con una connessione a parte, senza passare dalla Session dell'app."""
    checker = create_engine(settings.database_url.get_secret_value())
    with checker.connect() as connection:
        return connection.execute(text("SELECT count(*) FROM cineteca.reviews")).scalar_one()


if __name__ == "__main__":
    print("recensioni prima:", count_reviews())
    client = TestClient(app, raise_server_exceptions=False)
    body = {"rating": 4, "text": "Bello, lo rivedrei volentieri.", "has_spoilers": False}
    response = client.post("/movies/1/reviews", json=body)
    print("POST /movies/1/reviews ->", response.status_code)
    print("recensioni dopo:", count_reviews())
