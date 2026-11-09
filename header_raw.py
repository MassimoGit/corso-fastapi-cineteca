"""L'header X-Spectator letto senza i gestori di errore dell'app: il 422 grezzo di FastAPI."""
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/whoami")
def whoami(x_spectator: Annotated[str, Header()]) -> dict:
    return {"spectator": x_spectator}
