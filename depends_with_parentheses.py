"""Errore comune: Depends(get_settings()) con le parentesi."""
from typing import Annotated

from fastapi import Depends, FastAPI

from app.database import Settings, get_settings

app = FastAPI()

WrongSettingsDep = Annotated[Settings, Depends(get_settings())]


@app.get("/name")
def get_name(settings: WrongSettingsDep) -> dict:
    return {"name": settings.app_name}
