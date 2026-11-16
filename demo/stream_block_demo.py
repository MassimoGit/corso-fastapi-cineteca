"""Dimostrativo: un generatore che aspetta, scritto con def e con async def. Non fa parte dell'app della cineteca."""
import asyncio
import time
from collections.abc import AsyncIterator, Iterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


def sync_lines() -> Iterator[str]:
    for number in range(3):
        time.sleep(1)  # generatore normale: Starlette lo fa girare in un thread
        yield f"riga {number}\n"


async def async_lines_wrong() -> AsyncIterator[str]:
    for number in range(3):
        time.sleep(1)  # SBAGLIATO APPOSTA: generatore async con un'attesa che blocca l'event loop
        yield f"riga {number}\n"


async def async_lines_right() -> AsyncIterator[str]:
    for number in range(3):
        await asyncio.sleep(1)
        yield f"riga {number}\n"


@app.get("/sync-stream")
def sync_stream() -> StreamingResponse:
    return StreamingResponse(sync_lines(), media_type="text/plain")


@app.get("/async-stream-wrong")
def async_stream_wrong() -> StreamingResponse:
    return StreamingResponse(async_lines_wrong(), media_type="text/plain")


@app.get("/async-stream-right")
def async_stream_right() -> StreamingResponse:
    return StreamingResponse(async_lines_right(), media_type="text/plain")


@app.get("/fast")
def fast() -> dict:
    return {"route": "fast"}
