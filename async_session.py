"""Errore comune: una route async def con la Session sincrona. La query ferma tutto il server."""
from fastapi import FastAPI
from sqlalchemy import text

from app.dependencies import SessionDep

app = FastAPI()


@app.get("/slow-sync")
def slow_sync(session: SessionDep) -> dict:
    # pg_sleep(2): il database risponde dopo due secondi, come una query lenta
    session.execute(text("SELECT pg_sleep(2)"))
    return {"value": "done"}


@app.get("/slow-async")
async def slow_async(session: SessionDep) -> dict:
    session.execute(text("SELECT pg_sleep(2)"))  # SBAGLIATO: la Session è sincrona e blocca tutte le richieste
    return {"value": "done"}


@app.get("/fast")
def fast() -> dict:
    return {"value": "fast"}
