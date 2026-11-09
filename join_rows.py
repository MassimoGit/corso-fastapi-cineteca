"""Titolo e regista di ogni film: il SQL scritto a mano, poi la stessa query con l'ORM. Le righe non sono oggetti Movie."""
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Director, Movie

SQL = text("""
    SELECT m.title, d.name
    FROM cineteca.movies m
    JOIN cineteca.directors d ON d.director_id = m.director_id
    ORDER BY m.movie_id
""")

ORM = select(Movie.title, Director.name).join(Director).order_by(Movie.movie_id)

print(ORM)
print()

with Session(engine) as session:
    sql_rows = session.execute(SQL).all()
    rows = session.execute(ORM).all()
    print("tipo del risultato:", type(rows).__name__, "di", len(rows), "elementi, ognuno è una", type(rows[0]).__name__)
    print("prima riga:", rows[0])
    print("per posizione:", rows[0][0], "|", rows[0][1])
    print("per nome:", rows[0].title, "|", rows[0].name)
    for title, name in rows[:2]:
        print("spacchettata:", title, "-", name)
    print("uguale al SQL scritto a mano?", [tuple(r) for r in sql_rows] == [tuple(r) for r in rows])
    print("first():", session.execute(ORM).first())
    print("first(), nessun risultato:", session.execute(ORM.where(Movie.title == "Titanic")).first())
