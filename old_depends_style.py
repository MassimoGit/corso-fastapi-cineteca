"""La forma vecchia di Depends, con la dependency come valore predefinito. Funziona uguale."""
from fastapi import Depends, FastAPI

from app.dependencies import pagination

app = FastAPI()


@app.get("/movies")
def list_movies(page: dict = Depends(pagination)) -> dict:
    return page
