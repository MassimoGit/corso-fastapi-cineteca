"""Un report con due CTE, eseguito con text() e due parametri."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

engine = create_engine(os.getenv("DATABASE_URL"))

# Tempo medio di risoluzione, in ore, dei clienti con almeno :min_tickets ticket conclusi.
REPORT = text("""
    WITH conclusi AS (
        SELECT id_ticket, id_cliente,
               extract(epoch FROM chiuso_il - aperto_il) / 3600 AS ore
        FROM ticket
        WHERE chiuso_il IS NOT NULL
    ),
    per_cliente AS (
        SELECT id_cliente, count(*) AS ticket, round(avg(ore), 1) AS ore_medie
        FROM conclusi
        GROUP BY id_cliente
        HAVING count(*) >= :min_tickets
    )
    SELECT c.ragione_sociale, p.ticket, p.ore_medie
    FROM per_cliente p
    JOIN clienti c ON c.id_cliente = p.id_cliente
    ORDER BY p.ore_medie DESC
    LIMIT :top
""")

with engine.connect() as conn:
    for min_tickets, top in ((5, 5), (10, 3)):
        print(f"Almeno {min_tickets} ticket conclusi, primi {top}")
        for row in conn.execute(REPORT, {"min_tickets": min_tickets, "top": top}):
            print(f"  {row.ragione_sociale}: {row.ticket} ticket, {row.ore_medie} ore")
