"""Un modulo scritto in Pydantic v1, come main.py viene importato da Uvicorn e non lanciato direttamente."""
from pydantic import BaseModel, validator


class TrainerV1(BaseModel):
    name: str

    @validator("name")
    def lower_name(cls, value):
        return value.lower()

    class Config:
        orm_mode = True


print(TrainerV1.parse_obj({"name": "ASH"}).dict())
