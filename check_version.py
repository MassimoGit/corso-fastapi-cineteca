"""Legge la tabella cineteca.alembic_version per vedere a quale revisione è marcato il database."""
from sqlalchemy import text

from app.database import engine

with engine.connect() as conn:
    rows = conn.execute(text("SELECT version_num FROM cineteca.alembic_version")).scalars().all()
    print("alembic_version in cineteca:", rows)
