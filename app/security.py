"""Primitive crittografiche per le password (argon2id con pwdlib) e i JWT (PyJWT)."""
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

# argon2id con parametri consigliati dalla libreria; un oggetto solo condiviso per tutta l'app
password_hash = PasswordHash.recommended()

# Calcolato una volta all'avvio: serve al login per tenere uguale il tempo di risposta anche se l'utente non esiste
DUMMY_HASH = password_hash.hash("dummy-password-for-constant-time-login")


def hash_password(plain_password: str) -> str:
    """Trasforma una password in chiaro in una stringa argon2id con salt casuale."""
    return password_hash.hash(plain_password)


def verify_and_update_password(plain_password: str, stored_hash: str) -> tuple[bool, str | None]:
    """Verifica la password e restituisce anche l'eventuale nuovo hash se i parametri argon2 sono saliti."""
    return password_hash.verify_and_update(plain_password, stored_hash)


def create_access_token(
    subject: str,
    role: str,
    secret_key: str,
    algorithm: str = "HS256",
    expires_delta: timedelta | None = None,
) -> str:
    """Crea e firma un JWT con subject, ruolo, istante di emissione (iat) e scadenza (exp) in UTC."""
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=30))
    payload = {"sub": subject, "role": role, "iat": now, "exp": expire}
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_access_token(token: str, secret_key: str, algorithm: str = "HS256") -> dict:
    """Verifica firma, algoritmo atteso e presenza di exp e sub; solleva InvalidTokenError se qualcosa non torna."""
    return jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
        options={"require": ["exp", "sub"]},
    )
