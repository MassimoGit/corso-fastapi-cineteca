"""Errore comune: il gestore registrato per l'HTTPException di FastAPI non vede i 404 delle routes."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(HTTPException)
def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    raise HTTPException(status_code=404, detail=f"movie {movie_id} not found")
