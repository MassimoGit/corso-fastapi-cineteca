"""Una relationship non ancora caricata, letta dopo la chiusura della Session."""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Movie

with Session(engine, expire_on_commit=False) as session:
    movie = session.get(Movie, 1)
# qui la Session è chiusa: l'oggetto non è più legato a nessuna Session

print("titolo:", movie.title)  # una colonna già caricata si legge ancora
try:
    print("regista:", movie.director.name)  # una relationship non caricata no
except SQLAlchemyError as error:
    print(type(error).__name__)
    print(error)
