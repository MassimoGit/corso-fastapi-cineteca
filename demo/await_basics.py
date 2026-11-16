"""Dimostrativo: una coroutine, await e asyncio.run."""
import asyncio
import time


async def get_greeting() -> str:
    await asyncio.sleep(0.5)  # l'attesa: mentre dura, il programma può fare altro
    return "ciao"


async def main() -> None:
    start = time.perf_counter()
    greeting = await get_greeting()
    print(f"{greeting!r} dopo {time.perf_counter() - start:.1f} s")


asyncio.run(main())  # avvia l'event loop, esegue main() fino alla fine e lo chiude
