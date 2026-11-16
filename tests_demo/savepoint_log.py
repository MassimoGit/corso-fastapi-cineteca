"""Solo dimostrativo, non è un test: cosa manda al database una Session legata a una transaction esterna.

Si lancia con:  uv run python tests_demo/savepoint_log.py   (dalla cartella API09)
Crea lo schema cineteca_test, ci fa un commit dentro una transaction esterna, annulla tutto e cancella lo schema.
"""
import sys
from pathlib import Path

from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # la cartella API09, per "import app"

from app.database import settings
from app.models import Base, Director

engine = create_engine(settings.database_url.get_secret_value()).execution_options(
    schema_translate_map={"cineteca": "cineteca_test"}
)
with engine.begin() as setup:
    setup.execute(text("DROP SCHEMA IF EXISTS cineteca_test CASCADE"))
    setup.execute(text("CREATE SCHEMA cineteca_test"))
    Base.metadata.create_all(setup)

engine.echo = True  # da qui in poi il log SQL

print("--- il test comincia: connection e transaction esterna")
connection = engine.connect()
transaction = connection.begin()
session = Session(bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False)

print("--- la route aggiunge un regista e fa commit")
session.add(Director(name="Denis Villeneuve"))
session.commit()
print("--- il test legge: il regista c'è")
print("registi:", session.scalar(select(func.count()).select_from(Director)))

print("--- il test finisce: close, rollback della transaction esterna")
session.close()
transaction.rollback()
connection.close()

engine.echo = False
with engine.connect() as check:
    print("registi dopo il rollback:", check.scalar(select(func.count()).select_from(Director)))
with engine.begin() as cleanup:
    cleanup.execute(text("DROP SCHEMA cineteca_test CASCADE"))
