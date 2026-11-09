"""Errore comune: nell'alias manca Depends(...), quindi pagination non è una dependency."""
from typing import Annotated

from fastapi import FastAPI

from app.dependencies import pagination

app = FastAPI()

WrongPageDep = Annotated[dict, pagination]


@app.get("/movies")
def list_movies(page: WrongPageDep) -> dict:
    return page
