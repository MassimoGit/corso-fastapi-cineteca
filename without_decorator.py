"""La stessa API di first_app.py, registrata senza la chiocciola."""
from fastapi import FastAPI

app = FastAPI()


def root():
    return {"service": "Cineteca API", "version": 1}


app.add_api_route("/", root, methods=["GET"])
