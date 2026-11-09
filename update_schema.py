"""MovieUpdate: tutti i campi facoltativi. La trappola di `X | None` senza default."""
from pydantic import BaseModel, ValidationError


class WrongUpdate(BaseModel):
    title: str | None
    runtime_min: int | None
    plot: str | None


class MovieUpdate(BaseModel):
    title: str | None = None
    runtime_min: int | None = None
    plot: str | None = None


try:
    WrongUpdate.model_validate({"runtime_min": 150})
except ValidationError as error:
    print(error.error_count(), "errori:")
    for e in error.errors():
        print(" ", e["loc"], e["type"], "|", e["msg"])

print(MovieUpdate.model_validate({"runtime_min": 150}))
print(MovieUpdate.model_validate({}))
