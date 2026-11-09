"""L'ordine di una dependency con yield: prima la dependency, poi la route, poi il codice dopo yield."""
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()


def fake_session() -> Iterator[str]:
    print("  1. dependency: apro la session")
    try:
        yield "session"
    finally:
        print("  3. dependency: chiudo la session")


def careless_session() -> Iterator[str]:
    """Lo stesso, ma senza try / finally."""
    print("  1. dependency: apro la session")
    yield "session"
    print("  3. dependency: chiudo la session")


FakeDep = Annotated[str, Depends(fake_session)]
CarelessDep = Annotated[str, Depends(careless_session)]


@app.get("/ok")
def ok(session: FakeDep) -> dict:
    print("  2. route: lavoro con la session")
    return {"result": "ok"}


@app.get("/not-found")
def not_found(session: FakeDep) -> dict:
    print("  2. route: sollevo HTTPException")
    raise HTTPException(status_code=404, detail="not here")


@app.get("/crash")
def crash(session: FakeDep) -> dict:
    print("  2. route: sollevo ValueError")
    raise ValueError("boom")


@app.get("/crash-careless")
def crash_careless(session: CarelessDep) -> dict:
    print("  2. route: sollevo ValueError")
    raise ValueError("boom")


if __name__ == "__main__":
    client = TestClient(app, raise_server_exceptions=False)
    for path in ("/ok", "/not-found", "/crash", "/crash-careless"):
        print(f"GET {path}")
        response = client.get(path)
        print(f"  -> {response.status_code}")
