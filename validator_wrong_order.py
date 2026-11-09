"""Errore comune: @classmethod scritto sopra @field_validator."""
from pydantic import BaseModel, field_validator


class MovieCreate(BaseModel):
    title: str

    @classmethod
    @field_validator("title")
    def clean_title(cls, value: str) -> str:
        return " ".join(value.split())


print(repr(MovieCreate(title="  La   vita è bella ").title))
