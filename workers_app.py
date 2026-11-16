"""Ogni worker ha il suo pool: la route dice quale processo risponde e con quale connessione al database."""
import os

from fastapi import FastAPI
from sqlalchemy import text

from app.dependencies import SessionDep

app = FastAPI()


@app.get("/who")
def who(session: SessionDep) -> dict:
    connection = session.scalar(text("SELECT pg_backend_pid()"))  # la connessione sul server
    session.execute(text("SELECT pg_sleep(1)"))  # la tiene occupata, così le richieste si sovrappongono
    return {"worker": os.getpid(), "connection": connection}  # os.getpid() è l'id del processo che risponde
