"""Una condizione SQL non è un booleano di Python: if e and non funzionano."""
from models import Movie

try:
    if Movie.runtime_min > 150:
        print("lungo")
except TypeError as error:
    print("if:", type(error).__name__ + ":", error)

try:
    condition = Movie.runtime_min > 150 and Movie.release_year >= 2000
except TypeError as error:
    print("and:", type(error).__name__ + ":", error)

# Giusto: and_() oppure più condizioni dentro where(), oppure l'operatore & con le parentesi.
print((Movie.runtime_min > 150) & (Movie.release_year >= 2000))
