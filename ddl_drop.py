"""Cancella lo schema di prova e controlla che cineteca sia rimasta com'era."""
from sqlalchemy import text

from app.database import engine

DEMO_SCHEMA = "cineteca_ddl_demo"
assert DEMO_SCHEMA != "cineteca"

with engine.connect() as conn:
    conn.execute(text(f"DROP SCHEMA IF EXISTS {DEMO_SCHEMA} CASCADE"))
    conn.commit()
    demo = conn.execute(text("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'cineteca_ddl_demo'"))
    real = conn.execute(text("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'cineteca'"))
    print("tabelle in cineteca_ddl_demo:", demo.scalar())
    print("tabelle in cineteca:", real.scalar())
