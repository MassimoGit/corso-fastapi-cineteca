"""Pydantic senza FastAPI: un modello che controlla una recensione."""
from typing import TypedDict

from pydantic import BaseModel, Field, ValidationError


class ReviewDict(TypedDict):
    author: str
    rating: int
    text: str


class Review(BaseModel):
    author: str = Field(pattern=r"^[a-z0-9_]{3,20}$")
    rating: int = Field(ge=1, le=5)
    text: str = Field(min_length=10, max_length=500)
    has_spoilers: bool = False


# Il TypedDict descrive, ma non controlla: questo dizionario sbagliato passa.
wrong: ReviewDict = {"author": "Al", "rating": "tantissimo", "text": "bello"}
print(wrong)

# Il modello Pydantic controlla e converte.
good = Review(author="giulia_88", rating="4", text="Lungo ma ne vale la pena.")
print(good)
print(good.rating + 1)
print(good.model_dump())
print(good.model_dump_json())

from_website = {"author": "marco", "rating": 5, "text": "Il finale non te lo aspetti.", "has_spoilers": "true"}
print(Review.model_validate(from_website))

try:
    Review(author="Al", rating="tantissimo", text="bello")
except ValidationError as error:
    print(error.error_count(), "errori")
    for e in error.errors():
        print(e["loc"], e["type"], "|", e["msg"])
