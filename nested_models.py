"""Schemi annidati: un field può essere un altro schema o una lista di schemi."""
from pydantic import BaseModel, ValidationError


class DirectorRead(BaseModel):
    director_id: int
    name: str


class ActorRead(BaseModel):
    name: str
    character_name: str


class MovieDetail(BaseModel):
    movie_id: int
    title: str
    director: DirectorRead
    cast: list[ActorRead]


# Dati scritti a mano, come se arrivassero da un client.
data = {
    "movie_id": 1,
    "title": "Interstellar",
    "director": {"director_id": 1, "name": "Christopher Nolan"},
    "cast": [
        {"name": "Matthew McConaughey", "character_name": "Joseph Cooper"},
        {"name": "Anne Hathaway", "character_name": "Amelia Brand"},
    ],
}

movie = MovieDetail.model_validate(data)
print(movie)
print(type(movie.director).__name__, "-", movie.director.name)
print(type(movie.cast[0]).__name__, "-", movie.cast[0].character_name)
print(movie.model_dump_json())

broken = {**data, "director": {"director_id": 1}, "cast": [{"name": "Anne Hathaway", "character_name": 5}]}
try:
    MovieDetail.model_validate(broken)
except ValidationError as error:
    for e in error.errors():
        print(e["loc"], e["type"])
