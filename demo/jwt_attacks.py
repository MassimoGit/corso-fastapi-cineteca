"""Attacchi al JWT (alg: none, algorithm confusion) e confronto simmetrico HS256 contro asimmetrico RS256. File dimostrativo."""
import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


HS_SECRET = "chiave-hs256-dimostrativa-32byte"
now = datetime.now(timezone.utc)
valid_payload_b64 = b64url(json.dumps({"sub": "sara_staff", "role": "admin", "exp": int((now + timedelta(minutes=5)).timestamp())}).encode())

# 1. Attacco alg: none (token senza firma)
none_header = b64url(json.dumps({"alg": "none", "typ": "JWT"}).encode())
none_token = f"{none_header}.{valid_payload_b64}."
for label, fn in [
    ("alg: none con algorithms=['HS256']", lambda: jwt.decode(none_token, HS_SECRET, algorithms=["HS256"])),
    ("ispezione senza verify_signature (SOLO DEBUG)", lambda: jwt.decode(none_token, options={"verify_signature": False})),
]:
    try:
        print(label, "->", fn())
    except jwt.PyJWTError as error:
        print(f"{label} -> {type(error).__name__}: {error}")

# 2. Chiave asimmetrica RS256 (privata firma, pubblica verifica)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
private_pem = private_key.private_bytes(
    serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
)
public_pem = private_key.public_key().public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
)

rs_token = jwt.encode({"sub": "sara_staff", "role": "staff", "exp": now + timedelta(minutes=5)}, private_pem, algorithm="RS256")
print("\nRS256 firmato con privata, verificato con pubblica:", jwt.decode(rs_token, public_pem, algorithms=["RS256"])["sub"])

# 3. Attacco algorithm confusion: l'attaccante firma in HS256 usando i byte della chiave PUBBLICA
hs_header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
forged_sig = b64url(hmac.new(public_pem, f"{hs_header}.{valid_payload_b64}".encode(), hashlib.sha256).digest())
confused_token = f"{hs_header}.{valid_payload_b64}.{forged_sig}"

for label, fn in [
    ("confusion bloccata da algorithms=['RS256']", lambda: jwt.decode(confused_token, public_pem, algorithms=["RS256"])),
    ("confusion bloccata anche se si leggesse alg dal header", lambda: jwt.decode(confused_token, public_pem, algorithms=[jwt.get_unverified_header(confused_token)["alg"]])),
]:
    try:
        fn()
    except jwt.PyJWTError as error:
        print(f"{label} -> {type(error).__name__}: {error}")
