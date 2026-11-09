"""L'API della cineteca, terza versione: status code, 404, 409, 204 e response_model."""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Cineteca API", version="0.3.0")

MOVIES = [
    {"movie_id": 1, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "runtime_min": 169, "purchase_price_eur": 1200},
    {"movie_id": 2, "title": "La vita è bella", "director": "Roberto Benigni", "release_year": 1997, "runtime_min": 116, "purchase_price_eur": 800},
    {"movie_id": 3, "title": "Il buono, il brutto, il cattivo", "director": "Sergio Leone", "release_year": 1966, "runtime_min": 178, "purchase_price_eur": 650},
    {"movie_id": 4, "title": "La città incantata", "director": "Hayao Miyazaki", "release_year": 2001, "runtime_min": 125, "purchase_price_eur": 950},
    {"movie_id": 5, "title": "Inception", "director": "Christopher Nolan", "release_year": 2010, "runtime_min": 148, "purchase_price_eur": 1100},
]


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    director: str = Field(min_length=1, max_length=100)
    release_year: int = Field(ge=1888, le=2100)
    runtime_min: int = Field(ge=1, le=600)
    purchase_price_eur: int = Field(ge=0)


class MovieRead(BaseModel):
    movie_id: int
    title: str
    director: str
    release_year: int
    runtime_min: int


def find_movie(movie_id: int) -> dict:
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie {movie_id} not found")


@app.get("/movies")
def list_movies() -> list[MovieRead]:
    return MOVIES


@app.get(
    "/movies/{movie_id}",
    response_model=MovieRead,
    responses={404: {"description": "The movie does not exist"}},
)
def get_movie(movie_id: int):
    return find_movie(movie_id)


@app.post("/movies", status_code=status.HTTP_201_CREATED, responses={409: {"description": "Movie already in the catalogue"}})
def create_movie(movie: MovieCreate) -> MovieRead:
    for existing in MOVIES:
        if existing["title"] == movie.title and existing["release_year"] == movie.release_year:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="movie already in the catalogue")
    saved = {"movie_id": max(m["movie_id"] for m in MOVIES) + 1}
    saved.update(movie.model_dump())
    MOVIES.append(saved)
    return saved


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    MOVIES.remove(find_movie(movie_id))
