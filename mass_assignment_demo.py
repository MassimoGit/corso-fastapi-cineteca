# Mass assignment: il client scrive campi che non doveva poter scrivere. App dimostrativa, senza database.
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict

app = FastAPI()
USERS: list[dict] = []  # nel progetto vero: la tabella users


class UserWrong(BaseModel):  # SBAGLIATO APPOSTA: lo stesso schema in ingresso, nel database e in uscita
    name: str
    hashed_password: str = "hash-segreto"
    is_admin: bool = False


@app.post("/wrong/users", status_code=201)
def create_user_wrong(user: UserWrong) -> UserWrong:
    USERS.append(user.model_dump())
    return user


class UserCreate(BaseModel):  # solo quello che il client ha il diritto di scrivere
    model_config = ConfigDict(extra="forbid")
    name: str


class UserRead(BaseModel):  # solo quello che il client ha il diritto di leggere
    name: str
    is_admin: bool


@app.post("/right/users", status_code=201)
def create_user_right(user: UserCreate) -> UserRead:
    USERS.append({"name": user.name, "hashed_password": "hash-segreto", "is_admin": False})  # decide il server
    return UserRead(**USERS[-1])


client = TestClient(app)
body = {"name": "mallory", "is_admin": True}
for route in ("/wrong/users", "/right/users"):
    response = client.post(route, json=body)
    print(f"POST {route} {body}: {response.status_code} {response.json()}")
print("nel database:", USERS)
