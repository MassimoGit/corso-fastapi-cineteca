"""L'API della cineteca, seconda versione: path parameter, query parameter e body con Pydantic."""
from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Cineteca API", version="0.2.0")

MOVIES = [
    {"movie_id": 1, "title": "Interstellar", "director": "Christopher Nolan", "release_year": 2014, "runtime_min": 169},
    {"movie_id": 2, "title": "La vita è bella", "director": "Roberto Benigni", "release_year": 1997, "runtime_min": 116},
    {"movie_id": 3, "title": "Il buono, il brutto, il cattivo", "director": "Sergio Leone", "release_year": 1966, "runtime_min": 178},
    {"movie_id": 4, "title": "La città incantata", "director": "Hayao Miyazaki", "release_year": 2001, "runtime_min": 125},
    {"movie_id": 5, "title": "Inception", "director": "Christopher Nolan", "release_year": 2010, "runtime_min": 148},
]

SCREENINGS = [
    {"screening_id": 1, "movie_id": 1, "room_code": "S1", "starts_at": "2026-11-06T21:15:00", "is_3d": False},
    {"screening_id": 2, "movie_id": 4, "room_code": "S2", "starts_at": "2026-11-06T18:00:00", "is_3d": False},
    {"screening_id": 3, "movie_id": 5, "room_code": "S1", "starts_at": "2026-11-07T21:00:00", "is_3d": True},
]

REVIEWS = []


class ReviewCreate(BaseModel):
    author: str = Field(pattern=r"^[a-z0-9_]{3,20}$")
    rating: int = Field(ge=1, le=5)
    text: str = Field(min_length=10, max_length=500)
    has_spoilers: bool = False


# Queste due vanno scritte prima di /movies/{movie_id}: le routes si provano nell'ordine in cui sono dichiarate.
@app.get("/movies/directors")
def count_by_director():
    counts = {}
    for movie in MOVIES:
        counts[movie["director"]] = counts.get(movie["director"], 0) + 1
    return counts


@app.get("/movies/search")
def search_movies(title: str):
    return [m for m in MOVIES if title.lower() in m["title"].lower()]


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in MOVIES:
        if movie["movie_id"] == movie_id:
            return movie
    return None


@app.get("/movies")
def list_movies(
    director: str | None = None,
    max_runtime: int = 300,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
):
    selected = [
        m for m in MOVIES
        if (director is None or m["director"] == director) and m["runtime_min"] <= max_runtime
    ]
    return selected[:limit]


@app.get("/screenings")
def list_screenings(is_3d: bool | None = None):
    return [s for s in SCREENINGS if is_3d is None or s["is_3d"] == is_3d]


@app.get("/rooms/{room_code}/screenings")
def list_room_screenings(room_code: Annotated[str, Path(pattern=r"^S[0-9]$")]):
    return [s for s in SCREENINGS if s["room_code"] == room_code]


@app.post("/movies/{movie_id}/reviews")
def create_review(movie_id: int, review: ReviewCreate, source: str = "web"):
    saved = {"review_id": len(REVIEWS) + 1, "movie_id": movie_id, "source": source}
    saved.update(review.model_dump())
    REVIEWS.append(saved)
    return saved


@app.get("/reviews")
def list_reviews():
    return REVIEWS
