"""Pydantic v1 accanto a v2, sullo stesso schema. Il codice vecchio gira ancora: ecco cosa dice."""
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator, validator
from pydantic.errors import PydanticUserError


class TrainerV1(BaseModel):
    name: str

    @validator("name")
    def lower_name(cls, value):
        return value.lower()

    class Config:
        orm_mode = True


class TrainerV2(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

    @field_validator("name")
    @classmethod
    def lower_name(cls, value: str) -> str:
        return value.lower()


class FakeRow:
    """Un oggetto con un attributo name, come lo sarebbe un oggetto ORM."""

    name = "ASH"


data = {"name": "ASH"}

print("--- v1")
old = TrainerV1.parse_obj(data)
print(old.dict())
print(old.json())
try:
    TrainerV1.from_orm(FakeRow())
except PydanticUserError as error:
    print("from_orm:", error.message)
try:
    TrainerV1.model_validate(FakeRow())
except ValidationError as error:
    print("model_validate:", error.errors()[0]["type"])

print("--- v2")
new = TrainerV2.model_validate(data)
print(new.model_dump())
print(new.model_dump_json())
print(TrainerV2.model_validate(FakeRow()))
