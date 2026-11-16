"""Legge le sale dalla tabella cineteca.rooms con il nuovo attributo is_accessible."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Room

with Session(engine) as session:
    rooms = session.scalars(select(Room).order_by(Room.room_id)).all()
    for room in rooms:
        print(f"{room.code} | {room.name:<18} | posti: {room.seats:<3} | accessibile: {room.is_accessible}")
