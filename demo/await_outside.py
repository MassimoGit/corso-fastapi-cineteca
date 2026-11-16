"""Dimostrativo SBAGLIATO APPOSTA: await in una funzione def."""
import asyncio


def sync_route():
    await asyncio.sleep(1)  # SBAGLIATO: await vuole una funzione async def
