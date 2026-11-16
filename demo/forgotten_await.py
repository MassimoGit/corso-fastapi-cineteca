"""Dimostrativo: una coroutine chiamata senza await non esegue niente."""
import asyncio


async def get_greeting() -> str:
    await asyncio.sleep(0.1)
    return "ciao"


async def main() -> None:
    wrong = get_greeting()  # SBAGLIATO APPOSTA: manca await
    print("senza await:", type(wrong).__name__, wrong)
    right = await get_greeting()
    print("con await:", right)


asyncio.run(main())
