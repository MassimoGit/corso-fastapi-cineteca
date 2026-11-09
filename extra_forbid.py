"""model_config: un campo sconosciuto ignorato in silenzio, poi rifiutato. E str_strip_whitespace."""
from pydantic import BaseModel, ConfigDict, ValidationError


class LooseUpdate(BaseModel):
    title: str | None = None
    runtime_min: int | None = None


class StrictUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = None
    runtime_min: int | None = None


body = {"runtim_min": 150}

loose = LooseUpdate.model_validate(body)
print("senza forbid:", loose, "- campi passati:", loose.model_fields_set)

try:
    StrictUpdate.model_validate(body)
except ValidationError as error:
    e = error.errors()[0]
    print("con forbid:  ", e["loc"], e["type"], "|", e["msg"])

print(repr(LooseUpdate(title="  Dune  ").title), "senza strip")
print(repr(StrictUpdate(title="  Dune  ").title), "con str_strip_whitespace")
