"""Una dependency dichiarata due volte nella stessa richiesta gira una volta sola."""
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()
calls = {"count": 0}


def counter() -> int:
    calls["count"] += 1
    return calls["count"]


def wrapper(value: Annotated[int, Depends(counter)]) -> int:
    return value


@app.get("/probe")
def probe(a: Annotated[int, Depends(counter)], b: Annotated[int, Depends(wrapper)]) -> dict:
    return {"a": a, "b": b, "calls": calls["count"]}
