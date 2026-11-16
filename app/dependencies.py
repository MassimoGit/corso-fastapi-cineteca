"""La dependency della Session, la stessa di API07B: una Session per richiesta, chiusa a richiesta finita."""
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import engine


def get_session() -> Iterator[Session]:
    """Una Session per richiesta: la usano le routes e si chiude a richiesta finita."""
    with Session(engine, expire_on_commit=False) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
