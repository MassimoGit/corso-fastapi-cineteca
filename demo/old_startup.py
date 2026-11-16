"""Dimostrativo: la forma vecchia di avvio e spegnimento, @app.on_event, che si trova ancora in rete."""
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
def start() -> None:
    print("avvio")


@app.on_event("shutdown")
def stop() -> None:
    print("spegnimento")
