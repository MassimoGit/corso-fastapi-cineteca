"""from_attributes: dall'oggetto ORM allo schema, dentro il with della session."""
from pydantic import BaseModel, ConfigDict, ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models import Movie


class MovieRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movie_id: int
    title: str
    release_year: int
    runtime_min: int
    plot: str | None


with Session(engine) as session:
    movie = session.get(Movie, 1)
    schema = MovieRead.model_validate(movie)
    short = [MovieRead.model_validate(m) for m in session.scalars(select(Movie).where(Movie.runtime_min < 130))]

print(type(schema).__name__, schema)
print(schema.model_dump_json())
print([(m.title, m.runtime_min) for m in short])

# Lo schema è un oggetto Pydantic qualunque: vive anche a session chiusa.
print("a session chiusa:", schema.title)

with Session(engine) as session:
    movie = session.get(Movie, 2)
    session.commit()  # gli attributi dell'oggetto scadono

try:
    MovieRead.model_validate(movie)
except ValidationError as error:
    first = error.errors()[0]
    print(error.error_count(), "errori, il primo:", first["loc"], first["type"])
    print(first["msg"])
