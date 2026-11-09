"""Cosa Pydantic converte e cosa no."""
from pydantic import BaseModel, ValidationError


class Rating(BaseModel):
    stars: int
    reviewer: str
    has_spoilers: bool = False


tries = [
    {"stars": "4", "reviewer": "giulia_88"},
    {"stars": 4.0, "reviewer": "giulia_88", "has_spoilers": "yes"},
    {"stars": 4.5, "reviewer": "giulia_88"},
    {"stars": 4, "reviewer": 88},
    {"stars": 4, "reviewer": "giulia_88", "has_spoilers": "si"},
]

for data in tries:
    try:
        print("ok:", Rating.model_validate(data))
    except ValidationError as error:
        first = error.errors()[0]
        print("no:", first["loc"], first["type"])
