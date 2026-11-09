"""model_validate su un oggetto ORM, con uno schema senza from_attributes."""
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from database import engine
from models import Movie


class MovieRead(BaseModel):
    movie_id: int
    title: str
    release_year: int
    runtime_min: int
    plot: str | None


with Session(engine) as session:
    movie = session.get(Movie, 1)
    print("oggetto ORM:", type(movie).__name__, "-", movie.title)
    try:
        MovieRead.model_validate(movie)
    except ValidationError as error:
        e = error.errors()[0]
        print(e["loc"], e["type"])
        print(e["msg"])
