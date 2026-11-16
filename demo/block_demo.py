"""Dimostrativo: tre modi di aspettare un secondo dentro una route. Non fa parte dell'app della cineteca."""
import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/sync-sleep")
def sync_sleep() -> dict:
    time.sleep(1)  # def: FastAPI la esegue in un thread, il server resta libero
    return {"route": "sync-sleep"}


@app.get("/async-time-sleep")
async def async_time_sleep() -> dict:
    time.sleep(1)  # SBAGLIATO APPOSTA: async def esegue la route sull'event loop, e time.sleep lo ferma
    return {"route": "async-time-sleep"}


@app.get("/async-asyncio-sleep")
async def async_asyncio_sleep() -> dict:
    await asyncio.sleep(1)  # giusto: mentre aspetta, l'event loop serve altre richieste
    return {"route": "async-asyncio-sleep"}


@app.get("/fast")
def fast() -> dict:
    return {"route": "fast"}
