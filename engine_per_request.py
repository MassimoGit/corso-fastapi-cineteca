"""Errore comune: un engine, quindi un pool, a ogni richiesta, confrontato con un engine solo per tutto il programma."""
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.database import settings

URL = settings.database_url.get_secret_value()


def read_pid_wrong() -> int:
    """SBAGLIATO: ogni chiamata crea un engine nuovo, con un pool vuoto e una connessione tutta da aprire."""
    engine = create_engine(URL)
    with Session(engine) as session:
        return session.scalar(text("SELECT pg_backend_pid()"))


shared_engine = create_engine(URL)  # GIUSTO: uno solo, a livello di modulo, come in app/database.py


def read_pid_right() -> int:
    with Session(shared_engine) as session:
        return session.scalar(text("SELECT pg_backend_pid()"))


for name, function in (("engine in ogni richiesta", read_pid_wrong), ("engine condiviso", read_pid_right)):
    started = time.perf_counter()
    pids = {function() for _ in range(5)}
    print(f"{name}: 5 richieste, connessioni diverse sul server: {len(pids)}, tempo {time.perf_counter() - started:.1f} s")
shared_engine.dispose()
