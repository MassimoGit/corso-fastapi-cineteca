"""Confronta lo schema creato da cineteca.sql con quello creato da create_all: colonne, constraint, id."""
from sqlalchemy import text

from app.database import engine

COLUMNS = """SELECT table_name, column_name, data_type FROM information_schema.columns
WHERE table_schema = :s AND table_name <> 'alembic_version'"""
CONSTRAINTS = """SELECT t.relname, c.conname, pg_get_constraintdef(c.oid) FROM pg_constraint c
JOIN pg_class t ON t.oid = c.conrelid JOIN pg_namespace n ON n.oid = t.relnamespace
WHERE n.nspname = :s AND c.contype <> 'n' AND t.relname <> 'alembic_version'"""
IDS = """SELECT table_name, column_name, column_default, is_identity FROM information_schema.columns
WHERE table_schema = :s AND column_name LIKE '%_id' AND ordinal_position = 1 ORDER BY table_name LIMIT 2"""


def read(query: str, schema: str) -> list[tuple]:
    with engine.connect() as conn:
        return [tuple(str(v).replace(f"{schema}.", "") for v in r) for r in conn.execute(text(query), {"s": schema})]


sql_cols, orm_cols = set(read(COLUMNS, "cineteca")), set(read(COLUMNS, "cineteca_ddl_demo"))
print(f"colonne: cineteca={len(sql_cols)}, create_all={len(orm_cols)} | diverse: {sorted(sql_cols ^ orm_cols)}")
sql_con, orm_con = set(read(CONSTRAINTS, "cineteca")), set(read(CONSTRAINTS, "cineteca_ddl_demo"))
print(f"constraint: cineteca={len(sql_con)}, create_all={len(orm_con)}")
for table, name, definition in sorted(sql_con - orm_con):
    print(f"  manca o cambia in create_all: {table}.{name} -> {definition}")
print("id in cineteca.sql:", read(IDS, "cineteca"))
print("id in create_all:  ", read(IDS, "cineteca_ddl_demo"))
