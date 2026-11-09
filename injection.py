"""SQL injection: la stessa ricerca per ragione sociale, scritta male e scritta bene."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))


def search_wrong(conn, name):
    """SBAGLIATO: il testo scritto dall'utente finisce dentro la query."""
    query = f"SELECT ragione_sociale, piano FROM clienti WHERE ragione_sociale = '{name}'"
    return conn.execute(text(query)).all()


def search_right(conn, name):
    """GIUSTO: il testo viaggia come parametro, separato dalla query."""
    query = text("SELECT ragione_sociale, piano FROM clienti WHERE ragione_sociale = :name")
    return conn.execute(query, {"name": name}).all()


attack = "' OR '1'='1"

with engine.connect() as conn:
    print("nome normale, f-string:", search_wrong(conn, "Hotel Le Dune"))
    print("nome normale, parametro:", search_right(conn, "Hotel Le Dune"))

    rows = search_wrong(conn, attack)
    print("attacco, f-string:", len(rows), "clienti, il primo:", rows[0])
    print("attacco, parametro:", search_right(conn, attack))

with engine.connect() as conn:
    try:
        search_wrong(conn, "Pasticceria dell'Angolo")
    except ProgrammingError as error:
        print("apostrofo, f-string:", type(error.orig).__name__)
        print(str(error.orig).splitlines()[0])

with engine.connect() as conn:
    print("apostrofo, parametro:", search_right(conn, "Pasticceria dell'Angolo"))
