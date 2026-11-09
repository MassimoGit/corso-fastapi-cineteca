"""Il codice di SQLAlchemy 1.x che si trova in rete, accanto al suo equivalente 2.x."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

print("--- 1. engine.execute")
try:
    engine.execute(text("SELECT 1"))  # forma 1.x
except AttributeError as error:
    print("vecchio:", error)
with engine.connect() as conn:  # forma 2.x
    print("nuovo:", conn.execute(text("SELECT 1")).scalar())

print("--- 2. la query come semplice stringa")
with engine.connect() as conn:
    try:
        conn.execute("SELECT 1")  # forma 1.x
    except Exception as error:
        print("vecchio:", type(error).__name__, "-", error)
    print("nuovo:", conn.execute(text("SELECT 1")).scalar())

print("--- 3. l'autocommit di una volta")
INSERT = "INSERT INTO cineteca.rooms (code, name, seats) VALUES ('S12', 'Sala vecchio stile', 20)"
COUNT = text("SELECT count(*) FROM cineteca.rooms WHERE code = 'S12'")

with engine.connect() as conn:
    conn.execute(text(INSERT).execution_options(autocommit=True))  # forma 1.x
with engine.connect() as conn:
    print("vecchio: sale S12 presenti dopo l'INSERT:", conn.execute(COUNT).scalar())

with engine.begin() as conn:  # forma 2.x: la transaction si chiude da sola con un commit
    conn.execute(text(INSERT))
with engine.connect() as conn:
    print("nuovo: sale S12 presenti dopo l'INSERT:", conn.execute(COUNT).scalar())

with engine.begin() as conn:  # pulizia, così lo script si può rilanciare
    conn.execute(text("DELETE FROM cineteca.rooms WHERE code = 'S12'"))

print("--- 4. il driver nell'URL")
for url in (
    "postgresql://mario_rossi:LA_TUA_PASSWORD@pg.abacons.net:5432/mario_rossi",
    "postgresql+psycopg://mario_rossi:LA_TUA_PASSWORD@pg.abacons.net:5432/mario_rossi",
):
    print(url.split("://")[0], "->", create_engine(url).dialect.driver)

try:
    create_engine("postgresql+psycopg2://mario_rossi:LA_TUA_PASSWORD@pg.abacons.net:5432/mario_rossi")
except ModuleNotFoundError as error:
    print("postgresql+psycopg2 ->", type(error).__name__ + ":", error)

engine.dispose()
