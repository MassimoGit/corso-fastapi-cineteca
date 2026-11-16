"""Anatomia di un JWT e verifica a mano della firma HMAC-SHA256. File dimostrativo."""
import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

import jwt

SECRET = "chiave-dimostrativa-per-capire-jwt"


def b64url_decode(segment: str) -> bytes:
    """Decodifica base64url rimettendo il riempimento '=' che il formato JWT omette."""
    return base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))


now = datetime(2026, 11, 14, 14, 0, tzinfo=timezone.utc)
token = jwt.encode(
    {"sub": "sara_staff", "role": "staff", "iat": now, "exp": now + timedelta(minutes=30)},
    SECRET,
    algorithm="HS256",
)
header_b64, payload_b64, signature_b64 = token.split(".")

print("jwt completo:")
print(token)
print("\nle tre parti divise al punto:")
print("1) header :", header_b64)
print("2) payload:", payload_b64)
print("3) firma  :", signature_b64)

print("\ndecodificato da chiunque, senza nessuna chiave:")
print("header :", json.loads(b64url_decode(header_b64)))
print("payload:", json.loads(b64url_decode(payload_b64)))

# Ricalcolo a mano della firma HMAC-SHA256 sui primi due segmenti
signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
expected_mac = hmac.new(SECRET.encode("utf-8"), signing_input, hashlib.sha256).digest()
expected_b64 = base64.urlsafe_b64encode(expected_mac).decode("ascii").rstrip("=")
print("\nfirma ricalcolata a mano == terza parte del JWT?", hmac.compare_digest(expected_b64, signature_b64))

# Manomissione del payload senza conoscere SECRET: la firma non torna più
forged_payload = base64.urlsafe_b64encode(
    json.dumps({"sub": "sara_staff", "role": "admin", "exp": int((now + timedelta(minutes=30)).timestamp())}).encode()
).decode().rstrip("=")
forged_token = f"{header_b64}.{forged_payload}.{signature_b64}"
try:
    jwt.decode(forged_token, SECRET, algorithms=["HS256"])
except jwt.InvalidTokenError as error:
    print(f"payload cambiato in admin, stessa firma -> {type(error).__name__}: {error}")
