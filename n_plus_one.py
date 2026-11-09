"""Il problema N+1: una query per l'elenco dei registi e una in più per i film di ognuno."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine
from app.models import Director

with Session(engine) as session:
    directors = session.scalars(select(Director).order_by(Director.director_id)).all()
    print("registi caricati:", len(directors))
    for director in directors:
        print(f"{director.name}: {len(director.movies)} film")
