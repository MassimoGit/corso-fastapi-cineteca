"""Le eccezioni del dominio della cineteca e il modo in cui diventano risposte HTTP."""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class MovieNotFoundError(Exception):
    """Il film cercato non è nel catalogo."""

    def __init__(self, movie_id: int):
        super().__init__(f"movie {movie_id} not found")


class RoomNotFoundError(Exception):
    """La sala cercata non esiste."""

    def __init__(self, code: str):
        super().__init__(f"room {code} not found")


class MovieConflictError(Exception):
    """Il database ha rifiutato il film: titolo e anno già presenti, oppure regista che non esiste."""

    def __init__(self):
        super().__init__("movie already in the catalogue or director_id not found")


class DirectorConflictError(Exception):
    """Esiste già un regista con questo nome."""

    def __init__(self, name: str):
        super().__init__(f"director {name} already exists")


class SpectatorConflictError(Exception):
    """Esiste già uno spettatore con questo nome."""

    def __init__(self, name: str):
        super().__init__(f"spectator {name} already exists")


# Quale status HTTP corrisponde a quale eccezione del dominio. È l'unico punto che conosce entrambi i mondi.
STATUS_BY_ERROR = {
    MovieNotFoundError: status.HTTP_404_NOT_FOUND,
    RoomNotFoundError: status.HTTP_404_NOT_FOUND,
    MovieConflictError: status.HTTP_409_CONFLICT,
    DirectorConflictError: status.HTTP_409_CONFLICT,
    SpectatorConflictError: status.HTTP_409_CONFLICT,
}


def handle_domain_error(request: Request, exc: Exception):
    return JSONResponse(status_code=STATUS_BY_ERROR[type(exc)], content={"detail": str(exc)})


def handle_validation_error(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        # loc è ("path", "movie_id"), ("body", "title") oppure ("body",): la sorgente si toglie
        parts = error["loc"][1:] or error["loc"]
        field = ".".join(str(part) for part in parts)
        if field not in errors:
            errors[field] = []
        errors[field].append(error["msg"].removeprefix("Value error, "))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": "validation failed", "errors": errors},
    )


def register_error_handlers(app: FastAPI) -> None:
    """Collega ogni eccezione al suo gestore. add_exception_handler è ciò che fa la chiocciola @app.exception_handler."""
    for error_class in STATUS_BY_ERROR:
        app.add_exception_handler(error_class, handle_domain_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
