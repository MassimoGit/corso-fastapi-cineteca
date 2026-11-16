"""Claim registrati (RFC 7519), validazione in PyJWT e confronto datetime.now(timezone.utc) contro utcnow(). File dimostrativo."""
import warnings
from datetime import datetime, timedelta, timezone

import jwt

SECRET = "chiave-dimostrativa-per-claim-jwt"

# Confronto UTC: utcnow() restituisce un datetime naive che .timestamp() tratta come ora locale
aware = datetime.now(timezone.utc)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    naive = datetime.utcnow()
print("now(timezone.utc) timestamp:", int(aware.timestamp()))
print("utcnow().timestamp() errato:", int(naive.timestamp()))
print("differenza in secondi:", int(aware.timestamp() - naive.timestamp()))

now = datetime.now(timezone.utc)
full_token = jwt.encode(
    {
        "sub": "sara_staff",
        "iss": "cineteca-auth",
        "aud": "cineteca-api",
        "jti": "tok-01",
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=30),
    },
    SECRET,
    algorithm="HS256",
)
decoded = jwt.decode(
    full_token,
    SECRET,
    algorithms=["HS256"],
    issuer="cineteca-auth",
    audience="cineteca-api",
    options={"require": ["exp", "sub"]},
)
print("\nclaim completi verificati:", decoded)

# Casi di rifiuto controllati da PyJWT
expired = jwt.encode({"sub": "sara_staff", "exp": now - timedelta(seconds=5)}, SECRET, algorithm="HS256")
slightly_expired = jwt.encode({"sub": "sara_staff", "exp": now - timedelta(seconds=3)}, SECRET, algorithm="HS256")
future_nbf = jwt.encode({"sub": "sara_staff", "nbf": now + timedelta(seconds=60), "exp": now + timedelta(minutes=5)}, SECRET, algorithm="HS256")
int_sub = jwt.encode({"sub": 42, "exp": now + timedelta(minutes=5)}, SECRET, algorithm="HS256")
missing_exp = jwt.encode({"sub": "sara_staff"}, SECRET, algorithm="HS256")

checks = [
    ("token scaduto da 5 s", lambda: jwt.decode(expired, SECRET, algorithms=["HS256"])),
    ("scaduto da 3 s ma leeway=10", lambda: jwt.decode(slightly_expired, SECRET, algorithms=["HS256"], leeway=10)),
    ("nbf nel futuro", lambda: jwt.decode(future_nbf, SECRET, algorithms=["HS256"])),
    ("sub numerico invece di str", lambda: jwt.decode(int_sub, SECRET, algorithms=["HS256"])),
    ("issuer diverso", lambda: jwt.decode(full_token, SECRET, algorithms=["HS256"], issuer="altro")),
    ("audience diversa", lambda: jwt.decode(full_token, SECRET, algorithms=["HS256"], audience="altro")),
    ("manca exp obbligatorio", lambda: jwt.decode(missing_exp, SECRET, algorithms=["HS256"], options={"require": ["exp", "sub"]})),
]
print("\ncontrolli sui claim:")
for label, check in checks:
    try:
        res = check()
        print(f"  {label}: accettato -> sub={res['sub']}")
    except jwt.PyJWTError as error:
        print(f"  {label}: {type(error).__name__}: {error}")
