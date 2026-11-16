"""create_all non modifica le tabelle esistenti: la colonna aggiunta alla classe non arriva nel database."""
from sqlalchemy import MetaData, String, false, select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from app.database import engine


class DemoBase(DeclarativeBase):
    metadata = MetaData(schema="cineteca_ddl_demo")


class Room(DemoBase):
    __tablename__ = "rooms"
    room_id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(50))
    seats: Mapped[int]
    is_accessible: Mapped[bool] = mapped_column(server_default=false())


DemoBase.metadata.create_all(engine)
print("create_all eseguita senza errori")
with Session(engine) as session:
    try:
        session.scalars(select(Room)).all()
    except ProgrammingError as error:
        print("la prima select:", type(error.orig).__name__)
        print(str(error.orig).splitlines()[0])
