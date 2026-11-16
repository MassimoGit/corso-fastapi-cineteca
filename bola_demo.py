# BOLA: un utente autenticato legge le prenotazioni degli altri. App dimostrativa, senza database.
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient

TOKENS = {"token-di-giulia": "giulia_88", "token-di-luca": "luca_77"}  # nel progetto vero: la tabella spectators
BOOKINGS = {  # nel progetto vero: la tabella bookings, con la Foreign Key verso lo spettatore
    1: {"spectator": "giulia_88", "screening": "S1", "seats": 2},
    2: {"spectator": "luca_77", "screening": "S1", "seats": 4},
}

app = FastAPI()
bearer = HTTPBearer()


def get_spectator(credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]) -> str:
    if credentials.credentials not in TOKENS:
        raise HTTPException(401, detail="invalid spectator token", headers={"WWW-Authenticate": "Bearer"})
    return TOKENS[credentials.credentials]


@app.get("/wrong/bookings/{booking_id}")  # SBAGLIATO APPOSTA: controlla chi sei, non di chi è la prenotazione
def read_booking_wrong(booking_id: int, spectator: Annotated[str, Depends(get_spectator)]):
    return BOOKINGS[booking_id]


@app.get("/right/bookings/{booking_id}")
def read_booking_right(booking_id: int, spectator: Annotated[str, Depends(get_spectator)]):
    booking = BOOKINGS.get(booking_id)
    if booking is None or booking["spectator"] != spectator:
        raise HTTPException(404, detail=f"booking {booking_id} not found")  # non si dice nemmeno che esiste
    return booking


client = TestClient(app)
as_giulia = {"Authorization": "Bearer token-di-giulia"}
for route, booking_ids in (("/wrong", (1, 2)), ("/right", (1, 2, 3))):
    for booking_id in booking_ids:
        response = client.get(f"{route}/bookings/{booking_id}", headers=as_giulia)
        print(f"GET {route}/bookings/{booking_id} come giulia_88: {response.status_code} {response.json()}")
