"""Errore da non fare: session.execute restituisce righe (Row), non gli oggetti Room."""
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine
from models import Room

app = FastAPI()


class RoomRead(BaseModel):
    room_id: int
    code: str
    name: str
    seats: int


@app.get("/rooms")
def list_rooms() -> list[RoomRead]:
    query = select(Room).order_by(Room.room_id)
    with Session(engine) as session:
        return session.execute(query).all()  # SBAGLIATO: serve session.scalars(query).all()
