"""Una route lenta per vedere il pool al lavoro: ogni richiesta in corso tiene una connessione."""
from fastapi import FastAPI
from sqlalchemy import text

from app.dependencies import SessionDep

app = FastAPI()


@app.get("/slow")
def slow(session: SessionDep) -> dict:
    session.execute(text("SELECT pg_sleep(2)"))  # la Session prende la connessione e la tiene per due secondi
    return {"value": "done"}
