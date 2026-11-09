"""Le relationship: dal film al regista e dal regista ai suoi film, senza scrivere il join."""
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Movie

with Session(engine) as session:
    movie = session.get(Movie, 1)
    print("film:", movie.title)

    print("regista:", movie.director.name)  # la SELECT parte qui, alla prima lettura
    print("regista, seconda lettura:", movie.director.name)  # niente SELECT: l'oggetto c'è già

    print("film dello stesso regista:", [m.title for m in movie.director.movies])  # un'altra SELECT
    print("il primo è lo stesso oggetto di partenza?", movie.director.movies[0] is movie)
