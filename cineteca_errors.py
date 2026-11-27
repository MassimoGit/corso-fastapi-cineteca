"""La cineteca con una forma sola per tutti gli errori: {"error": ...}."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Cineteca API", version="0.3.1")

MOVIES = [
    {"movie_id": 1, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "runtime_min": 169},
    {"movie_id": 4, "title": "La città incantata", "director": "Hayao Miyazaki", "release_year": 2001, "runtime_min": 125},
]


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
    first = exc.errors()[0]
    where = ".".join(str(part) for part in first["loc"])
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"error": f"{where}: {first['msg']}"},
    )


def find_movie(movie_id: int) -> dict:
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    raise MovieNotFoundError(movie_id)


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int) -> MovieRead:
    return find_movie(movie_id)
