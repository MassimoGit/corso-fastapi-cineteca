"""mode="before" contro mode="after": cosa vede ciascun validator, e in che ordine."""
from pydantic import BaseModel, Field, ValidationError, field_validator


class MovieCreate(BaseModel):
    runtime_min: int = Field(ge=1, le=600)

    @field_validator("runtime_min", mode="before")
    @classmethod
    def read_minutes(cls, value):
        print("  before riceve:", repr(value))
        if isinstance(value, str) and value.endswith(" min"):
            return value.removesuffix(" min")
        return value

    @field_validator("runtime_min", mode="after")
    @classmethod
    def check_value(cls, value: int) -> int:
        print("  after riceve: ", repr(value))
        return value


for raw in ["148", "148 min", 148, "0 min", "lungo"]:
    print(repr(raw))
    try:
        print("  ->", MovieCreate(runtime_min=raw))
    except ValidationError as error:
        print("  ->", error.errors()[0]["type"])
