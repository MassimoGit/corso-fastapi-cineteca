"""Errore comune: il validator che dimentica il return."""
from pydantic import BaseModel, field_validator


class MovieCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("title cannot be blank")


movie = MovieCreate(title="  Dune  ")
print(repr(movie.title))
print(movie)
