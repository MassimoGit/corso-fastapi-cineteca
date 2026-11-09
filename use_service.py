"""Il servizio provato da uno script: nessun FastAPI, nessun HTTP."""
from app.errors import MovieConflictError, MovieNotFoundError
from app.schemas import MovieCreate
from app.services import movies as movies_service

inception = MovieCreate(title="Inception", director_id=1, release_year=2010, runtime_min=148, purchase_price_eur=1100)
try:
    movies_service.create_movie(inception)
except MovieConflictError as error:
    print("rifiutato:", error)

dune = MovieCreate(title="Dune", director_id=1, release_year=2021, runtime_min=155, purchase_price_eur=1300)
saved = movies_service.create_movie(dune)
print("salvato:", saved.movie_id, saved.title)

try:
    movies_service.get_movie(99)
except MovieNotFoundError as error:
    print("non trovato:", error)
