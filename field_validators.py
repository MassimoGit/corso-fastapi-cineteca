"""@field_validator: il titolo ripulito e controllato."""
from pydantic import BaseModel, Field, ValidationError, field_validator


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("title cannot be blank")
        return cleaned


for raw in ["  La   vita \t è bella ", "Dune", "     ", ""]:
    try:
        print(repr(raw), "->", repr(MovieCreate(title=raw).title))
    except ValidationError as error:
        e = error.errors()[0]
        print(repr(raw), "->", e["loc"], e["type"], "|", e["msg"])
