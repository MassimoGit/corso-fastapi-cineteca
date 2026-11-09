"""Il percorso "/" dentro un router con prefix: la route diventa /movies/ e /movies viene rimandato lì."""
from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/")
def list_movies() -> list[str]:
    return ["Interstellar", "Inception"]


app = FastAPI()
app.include_router(router)
