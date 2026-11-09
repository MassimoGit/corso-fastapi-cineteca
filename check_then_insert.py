"""Due richieste insieme: "prima cerco, poi inserisco" non basta, il constraint sì.

Le due richieste sono simulate con due session, nell'ordine in cui si possono intrecciare due richieste vere.
"""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Movie

TITLE, YEAR = "Nuovo Cinema Paradiso", 1988


def find(session: Session) -> Movie | None:
    return session.scalar(select(Movie).where(Movie.title == TITLE, Movie.release_year == YEAR))


def new_movie() -> Movie:
    return Movie(title=TITLE, director_id=1, release_year=YEAR, runtime_min=155, purchase_price_eur=700)


with Session(engine) as first, Session(engine) as second:
    print("richiesta A cerca il film:", find(first))
    print("richiesta B cerca il film:", find(second))  # il film non c'è ancora, nemmeno per B

    first.add(new_movie())
    first.commit()
    print("richiesta A inserisce e fa commit")

    second.add(new_movie())  # B ha controllato prima: per lei il film non c'era
    try:
        second.commit()
    except IntegrityError as error:
        print("richiesta B inserisce:", type(error.orig).__name__)
        print("constraint:", error.orig.diag.constraint_name)

    second.rollback()
    print("film nel catalogo:", len(second.scalars(select(Movie).where(Movie.title == TITLE)).all()))

    # Si rimette il catalogo com'era
    for movie in second.scalars(select(Movie).where(Movie.title == TITLE)):
        second.delete(movie)
    second.commit()
