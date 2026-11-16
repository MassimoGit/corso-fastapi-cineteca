"""Solo dimostrativo, non fa parte della cineteca: due chiavi con permessi diversi, per vedere 401 e 403 insieme.

Si lancia con:  uv run python tests_demo/forbidden_demo.py   (dalla cartella API10)
"""
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.testclient import TestClient

KEYS = {"reader-key": "reader", "admin-key": "admin"}  # chiave -> ruolo

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")


def find_role(api_key: str) -> str | None:
    for key, role in KEYS.items():
        if secrets.compare_digest(api_key.encode(), key.encode()):
            return role
    return None


def get_role(api_key: Annotated[str, Depends(api_key_header)]) -> str:
    """401: la chiave non è di nessuno, quindi non sappiamo chi sei."""
    role = find_role(api_key)
    if role is None:
        raise HTTPException(401, detail="invalid API key", headers={"WWW-Authenticate": "APIKey"})
    return role


def require_admin(role: Annotated[str, Depends(get_role)]) -> None:
    """403: sappiamo chi sei, e il tuo ruolo non basta."""
    if role != "admin":
        raise HTTPException(403, detail="this key cannot delete")


@app.get("/report")
def read_report(role: Annotated[str, Depends(get_role)]) -> dict:
    return {"report": "ok", "read_by": role}


@app.delete("/report", dependencies=[Depends(require_admin)])
def delete_report() -> dict:
    return {"report": "deleted"}


if __name__ == "__main__":
    client = TestClient(app)
    for method, key in [("GET", None), ("GET", "wrong-key"), ("GET", "reader-key"), ("DELETE", "reader-key"), ("DELETE", "admin-key")]:
        response = client.request(method, "/report", headers={"X-API-Key": key} if key else {})
        print(f"{method} /report  (X-API-Key: {key})  ->  {response.status_code}  {response.json()}")
