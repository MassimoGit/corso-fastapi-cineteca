"""Dimostrativo: come si consuma un generatore asincrono con async for (di solito lo fa StreamingResponse)."""
import asyncio
import sys
import time

sys.path.insert(0, "..")  # per importare app.services dalla cartella API11

from app.services.assistant import fake_model


async def main() -> None:
    start = time.perf_counter()
    async for word in fake_model("ciao", 0.3):
        print(f"{time.perf_counter() - start:3.1f} s  {word!r}")


asyncio.run(main())
