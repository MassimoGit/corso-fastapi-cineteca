"""Errore comune: catturare il TimeoutError di Python invece di quello di SQLAlchemy."""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.database import settings

engine = create_engine(settings.database_url.get_secret_value(), pool_size=1, max_overflow=0, pool_timeout=1)

with Session(engine) as first:
    first.execute(text("SELECT 1"))  # occupa l'unica connessione del pool
    try:
        with Session(engine) as second:
            second.execute(text("SELECT 1"))
    except TimeoutError:  # SBAGLIATO: è il TimeoutError di Python, manca l'import da sqlalchemy.exc
        print("pool esaurito, riprova più tardi")
