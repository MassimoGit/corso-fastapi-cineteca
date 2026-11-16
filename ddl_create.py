"""create_all su uno schema a parte, cineteca_ddl_demo: mostra il DDL che i model generano. MAI su cineteca."""
from sqlalchemy import text

from app.database import engine
from app.models import Base

DEMO_SCHEMA = "cineteca_ddl_demo"
assert DEMO_SCHEMA != "cineteca"

# Lo schema di prova: si cancella e si ricrea, è solo nostro.
with engine.connect() as conn:
    conn.execute(text(f"DROP SCHEMA IF EXISTS {DEMO_SCHEMA} CASCADE"))
    conn.execute(text(f"CREATE SCHEMA {DEMO_SCHEMA}"))
    conn.commit()

# Le classi dicono "cineteca": schema_translate_map sostituisce il nome in ogni comando di questo engine.
demo_engine = engine.execution_options(schema_translate_map={"cineteca": DEMO_SCHEMA})

Base.metadata.create_all(demo_engine)
