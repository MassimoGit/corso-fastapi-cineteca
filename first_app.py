"""La prima API: un solo endpoint che risponde alla radice."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"service": "Cineteca API", "version": 1}
