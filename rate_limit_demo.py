# Rate limiting minimo: finestra fissa, in memoria, per indirizzo. App dimostrativa.
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.testclient import TestClient

LIMIT = 5  # richieste ...
WINDOW_SECONDS = 60  # ... ogni minuto, per ogni indirizzo
# shortcut: in memoria, vale per un solo processo e si azzera al riavvio; con più worker serve un archivio condiviso o il proxy
hits: dict[str, list[float]] = {}  # indirizzo -> istanti delle richieste recenti

app = FastAPI()


def check_rate_limit(request: Request) -> None:
    now = time.monotonic()
    address = request.client.host
    recent = [t for t in hits.get(address, []) if now - t < WINDOW_SECONDS]
    if len(recent) >= LIMIT:
        retry_after = int(WINDOW_SECONDS - (now - recent[0])) + 1
        raise HTTPException(429, detail="too many attempts", headers={"Retry-After": str(retry_after)})
    hits[address] = recent + [now]


@app.post("/login")
def login(request: Request):
    check_rate_limit(request)
    return {"ok": False}


client = TestClient(app)
for attempt in range(1, 8):
    response = client.post("/login")
    print(attempt, response.status_code, response.json(), response.headers.get("retry-after"))
