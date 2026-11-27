"""La cineteca con una forma sola per tutti gli errori: {"error": ...}."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Cineteca API", version="0.3.1")

MOVIES = [
    {"movie_id": 1, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "runtime_min": 169},
    {"movie_id": 4, "title": "La città incantata", "director": "Hayao Miyazaki", "release_year": 2001, "runtime_min": 125},
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


class MovieNotFoundError(Exception):
    """Il film cercato non è nel catalogo."""

    def __init__(self, movie_id: int):
        super().__init__(f"movie {movie_id} not found")
        self.movie_id = movie_id

"""Film non trovato gestice MovieNotFoundError """
@app.exception_handler(MovieNotFoundError)
def handle_movie_not_found(request: Request, exc: MovieNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": str(exc)})

"""Generico"""
@app.exception_handler(StarletteHTTPException)
def handle_http_exception(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail}, headers=exc.headers)

"""Gestisce la HTTP_422_UNPROCESSABLE_CONTENT per validazione fallita"""
@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        # loc è ("path", "movie_id"), ("body", "types", 0) oppure ("body",): la sorgente si toglie
        parts = error["loc"][1:] or error["loc"]
        field = ".".join(str(part) for part in parts)
        if field not in errors:
            errors[field] = []
        errors[field].append(error["msg"].removeprefix("Value error, "))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": "validation failed", "errors": errors},
    )


def find_movie(movie_id: int) -> dict:
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    raise MovieNotFoundError(movie_id)


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int) -> MovieRead:
    return find_movie(movie_id)


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate) -> MovieRead:
    saved = {"movie_id": max(m["movie_id"] for m in MOVIES) + 1}
    saved.update(movie.model_dump())
    MOVIES.append(saved)
    return saved
