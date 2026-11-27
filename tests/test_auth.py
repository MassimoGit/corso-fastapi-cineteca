"""I test su registrazione con argon2id, login OAuth2 su /token, JWT e autorizzazione per ruoli."""
from datetime import timedelta

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from sqlalchemy import select

from app.models import User
from app.security import create_access_token


def test_register_user_stores_argon2_hash_and_never_returns_password(client, session):
    response = client.post("/users", json={"username": "marco_staff", "password": "segreta-password-1"})
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "marco_staff"
    assert body["role"] == "staff"
    assert "password" not in body
    assert "hashed_password" not in body

    saved = session.scalar(select(User).where(User.username == "marco_staff"))
    assert saved is not None
    assert saved.hashed_password.startswith("$argon2id$")
    assert saved.hashed_password != "segreta-password-1"


def test_register_user_forbids_role_mass_assignment(client):
    response = client.post(
        "/users",
        json={"username": "mallory", "password": "segreta-password-1", "role": "admin"},
    )
    assert response.status_code == 422
    assert list(response.json()["errors"]) == ["role"]


def test_register_duplicate_username_returns_409(client):
    response = client.post("/users", json={"username": "sara_staff", "password": "altra-password-9"})
    assert response.status_code == 409
    assert response.json() == {"detail": "user sara_staff already exists"}


def test_login_returns_bearer_jwt_and_opens_users_me(client, test_settings):
    response = client.post("/token", data={"username": "sara_staff", "password": "cineteca-staff-99"})
    assert response.status_code == 200
    token_body = response.json()
    assert token_body["token_type"] == "bearer"

    claims = jwt.decode(
        token_body["access_token"],
        test_settings.jwt_secret_key.get_secret_value(),
        algorithms=["HS256"],
    )
    assert claims["sub"] == "sara_staff"
    assert claims["role"] == "staff"
    assert "exp" in claims and "iat" in claims

    me = client.get("/users/me", headers={"Authorization": f"Bearer {token_body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["username"] == "sara_staff"
    assert me.json()["role"] == "staff"


def test_login_gives_same_401_for_unknown_user_and_wrong_password(client):
    wrong_pass = client.post("/token", data={"username": "sara_staff", "password": "sbagliata"})
    unknown_user = client.post("/token", data={"username": "nessuno_99", "password": "sbagliata"})
    for response in (wrong_pass, unknown_user):
        assert response.status_code == 401
        assert response.json() == {"detail": "invalid username or password"}
        assert response.headers["www-authenticate"] == "Bearer"


def test_login_upgrades_outdated_argon2_hash_via_verify_and_update(client, session):
    legacy_hash = PasswordHash((Argon2Hasher(memory_cost=19456, time_cost=2, parallelism=1),)).hash(
        "vecchia-password-1"
    )
    user = User(username="paolo_vecchio", hashed_password=legacy_hash, role="staff")
    session.add(user)
    session.commit()

    response = client.post("/token", data={"username": "paolo_vecchio", "password": "vecchia-password-1"})
    assert response.status_code == 200
    session.refresh(user)
    assert user.hashed_password != legacy_hash
    assert "$m=65536," in user.hashed_password


def test_expired_tampered_and_wrong_secret_tokens_return_401(client, test_settings):
    secret = test_settings.jwt_secret_key.get_secret_value()
    expired = create_access_token("sara_staff", "staff", secret, expires_delta=timedelta(minutes=-5))
    valid = create_access_token("sara_staff", "staff", secret)
    header, payload, sig = valid.split(".")
    tampered = f"{header}.{payload}.{sig[:-4]}AAAA"
    wrong_secret = create_access_token("sara_staff", "staff", "chiave-completamente-diversa-32byte")

    for bad_token in (expired, tampered, wrong_secret, "non-un-jwt", "giulia-test-token"):
        response = client.get("/users/me", headers={"Authorization": f"Bearer {bad_token}"})
        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"


def test_token_of_deleted_user_returns_401(client, session, test_settings):
    user = session.scalar(select(User).where(User.username == "sara_staff"))
    token = create_access_token("sara_staff", "staff", test_settings.jwt_secret_key.get_secret_value())
    session.delete(user)
    session.commit()

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_admin_only_routes_return_403_to_staff_and_200_to_admin(staff_client, admin_client):
    assert staff_client.get("/stats/movies-per-director").status_code == 403
    assert staff_client.get("/users").status_code == 403
    assert admin_client.get("/stats/movies-per-director").status_code == 200
    users = admin_client.get("/users")
    assert users.status_code == 200
    assert [u["username"] for u in users.json()] == ["sara_staff", "elena_admin"]
