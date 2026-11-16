"""Dimostrativo: l'ordine di lifespan. Il prima e il dopo di yield intorno alla vita dell'app."""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("1. avvio: prima di yield")
    yield
    print("3. spegnimento: dopo yield")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root() -> dict:
    print("2. richiesta")
    return {"ok": True}


with TestClient(app) as client:  # with: il TestClient avvia e spegne l'app, come fa il server
    client.get("/")
