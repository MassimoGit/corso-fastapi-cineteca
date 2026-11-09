"""I film per regista: prima in SQL con text(), poi con l'ORM, e i due conteggi a confronto. Poi un regista senza film."""
from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Director, Movie

SQL = text("""
    SELECT d.name, count(*) AS movies
    FROM cineteca.movies m
    JOIN cineteca.directors d ON d.director_id = m.director_id
    GROUP BY d.name
    ORDER BY movies DESC, d.name
""")

INNER = (
    select(Director.name, func.count().label("movies"))
    .join(Movie)
    .group_by(Director.name)
    .order_by(func.count().desc(), Director.name)
)

OUTER = (
    select(Director.name, func.count(Movie.movie_id).label("movies"))
    .join(Movie, isouter=True)
    .group_by(Director.name)
    .order_by(func.count(Movie.movie_id).desc(), Director.name)
)

print(INNER)
print()

with Session(engine) as session:
    sql_rows = [tuple(row) for row in session.execute(SQL)]
    orm_rows = [tuple(row) for row in session.execute(INNER)]
    print("con text():", sql_rows)
    print("con l'ORM: ", orm_rows)
    print("uguali?", sql_rows == orm_rows)

    # Un regista nuovo, senza film. La transaction non viene confermata: a fine blocco sparisce.
    session.add(Director(name="Denis Villeneuve"))
    session.flush()
    print()
    print("join interno:", [tuple(row) for row in session.execute(INNER)])
    print()
    print(OUTER)
    print()
    print("join esterno:", [tuple(row) for row in session.execute(OUTER)])
    session.rollback()
