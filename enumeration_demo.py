# User enumeration: la risposta (e il tempo) dicono chi esiste. App dimostrativa, senza database.
import statistics
import time

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pwdlib import PasswordHash
from pydantic import BaseModel

password_hash = PasswordHash.recommended()
USERS = {"giulia_88": password_hash.hash("juventus")}  # nel progetto vero: la tabella users
DUMMY_HASH = password_hash.hash("password-che-nessuno-usa")  # calcolato una volta, all'avvio

app = FastAPI()


class Credentials(BaseModel):
    username: str
    password: str


@app.post("/login-wrong")  # SBAGLIATO APPOSTA: due messaggi, e un utente mancante costa meno
def login_wrong(credentials: Credentials):
    stored = USERS.get(credentials.username)
    if stored is None:
        raise HTTPException(404, detail="user not found")
    if not password_hash.verify(credentials.password, stored):
        raise HTTPException(401, detail="wrong password")
    return {"ok": True}


@app.post("/login-same-message")  # SBAGLIATO APPOSTA: un messaggio solo, ma il tempo tradisce
def login_same_message(credentials: Credentials):
    stored = USERS.get(credentials.username)
    if stored is None or not password_hash.verify(credentials.password, stored):
        raise HTTPException(401, detail="invalid username or password")
    return {"ok": True}


@app.post("/login-right")  # un solo messaggio, e il tempo è lo stesso
def login_right(credentials: Credentials):
    stored = USERS.get(credentials.username, DUMMY_HASH)  # senza utente si confronta con un hash finto
    if not password_hash.verify(credentials.password, stored) or credentials.username not in USERS:
        raise HTTPException(401, detail="invalid username or password")
    return {"ok": True}


client = TestClient(app)
client.post("/login-right", json={"username": "giulia_88", "password": "x"})  # prima chiamata scartata: avvio a freddo
for route in ("/login-wrong", "/login-same-message", "/login-right"):
    for username in ("giulia_88", "marco_00"):
        times = []
        for _ in range(11):
            start = time.perf_counter()
            response = client.post(route, json={"username": username, "password": "sbagliata"})
            times.append((time.perf_counter() - start) * 1000)
        print(f"{route} {username}: {response.status_code} {response.json()} mediana {statistics.median(times):.0f} ms")
