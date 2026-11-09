"""@model_validator: una regola che riguarda due campi insieme."""
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError, model_validator


class ScreeningCreate(BaseModel):
    movie_id: int = Field(ge=1)
    room_id: int = Field(ge=1)
    starts_at: datetime
    ends_at: datetime

    @model_validator(mode="after")
    def check_order(self):
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        return self


good = ScreeningCreate(movie_id=1, room_id=1, starts_at="2026-11-20T20:30:00+01:00", ends_at="2026-11-20T23:20:00+01:00")
print(good.starts_at, "->", good.ends_at)

try:
    ScreeningCreate(movie_id=1, room_id=1, starts_at="2026-11-20T20:30:00+01:00", ends_at="2026-11-20T19:00:00+01:00")
except ValidationError as error:
    e = error.errors()[0]
    print(e["loc"], e["type"], "|", e["msg"])

try:
    ScreeningCreate(movie_id=1, room_id=1, starts_at="2026-11-20T20:30:00+01:00", ends_at="stasera")
except ValidationError as error:
    print([(e["loc"], e["type"]) for e in error.errors()])
