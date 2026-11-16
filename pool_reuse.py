"""Cento richieste, dieci alla volta: quante connessioni apre il pool?"""
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.database import settings

engine = create_engine(settings.database_url.get_secret_value(), pool_size=3, max_overflow=2)


def request(number: int) -> int:
    """Una richiesta finta: prende una connessione, lavora un attimo, dice quale connessione ha usato."""
    with Session(engine) as session:
        session.execute(text("SELECT pg_sleep(0.2)"))  # il server aspetta 0,2 secondi, come una query lenta
        return session.scalar(text("SELECT pg_backend_pid()"))  # l'id della connessione sul server


with ThreadPoolExecutor(max_workers=10) as executor:  # dieci richieste in corso nello stesso momento
    connections = set(executor.map(request, range(100)))  # chiama request(0), request(1)... request(99)

print("richieste servite: 100")
print("connessioni aperte verso il server:", len(connections))
print("nel pool a lavoro finito:", engine.pool.status())
engine.dispose()  # chiude le connessioni del pool
