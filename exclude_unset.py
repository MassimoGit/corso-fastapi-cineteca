"""Tre corpi per PATCH: vuoto, un campo, un campo null. E cosa vede exclude_unset."""
from pydantic import BaseModel


class MovieUpdate(BaseModel):
    title: str | None = None
    runtime_min: int | None = None
    plot: str | None = None


bodies = {
    "corpo vuoto": {},
    "campo assente": {"runtime_min": 150},
    "campo null": {"plot": None},
}

for label, body in bodies.items():
    update = MovieUpdate.model_validate(body)
    print(f"{label}: body = {body}")
    print(f"  model_dump()                   -> {update.model_dump()}")
    print(f"  model_dump(exclude_unset=True) -> {update.model_dump(exclude_unset=True)}")
    print(f"  model_fields_set               -> {update.model_fields_set}")
