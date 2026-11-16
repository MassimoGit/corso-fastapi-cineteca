"""L'assistente finto: scrive la risposta una parola alla volta, come farebbe un modello vero."""
import asyncio
from collections.abc import AsyncIterator


async def fake_model(question: str, delay_s: float) -> AsyncIterator[str]:
    """Un generatore asincrono: dopo ogni attesa produce la parola successiva."""
    answer = f"Hai chiesto: {question}. Questa risposta è finta e arriva una parola alla volta, come in una chat."
    for word in answer.split():
        await asyncio.sleep(delay_s)  # l'attesa di un modello vero: mentre aspetta, il server serve gli altri
        yield word + " "
