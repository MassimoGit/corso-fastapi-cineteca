"""Dimostrativo: cosa succede a un generatore quando il client chiude la connessione."""
import asyncio
import time
from collections.abc import AsyncIterator, Iterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


async def async_words() -> AsyncIterator[str]:
    try:
        for number in range(20):
            await asyncio.sleep(0.5)
            print(f"[async] parola {number}", flush=True)
            yield f"parola {number}\n"
    finally:
        print("[async] generatore chiuso", flush=True)  # il blocco finally gira anche se il client se ne va


def sync_words() -> Iterator[str]:
    try:
        for number in range(20):
            time.sleep(0.5)
            print(f"[sync] parola {number}", flush=True)
            yield f"parola {number}\n"
    finally:
        print("[sync] generatore chiuso", flush=True)


@app.get("/async-words")
async def get_async_words() -> StreamingResponse:
    return StreamingResponse(async_words(), media_type="text/plain")


@app.get("/sync-words")
def get_sync_words() -> StreamingResponse:
    return StreamingResponse(sync_words(), media_type="text/plain")
