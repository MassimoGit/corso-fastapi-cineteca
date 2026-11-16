# HMAC: un testo firmato con un segreto, a mano con il modulo hmac. File dimostrativo.
import base64
import hashlib
import hmac
import secrets

SECRET = secrets.token_bytes(32)  # la chiave di firma: la conosce solo il server


def sign(payload: str) -> str:
    """Restituisce 'payload.firma', tutti e due in base64url."""
    body = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    signature = hmac.new(SECRET, body.encode(), hashlib.sha256).digest()
    return body + "." + base64.urlsafe_b64encode(signature).decode().rstrip("=")


def verify(token: str) -> bool:
    body, _, received = token.partition(".")
    expected = hmac.new(SECRET, body.encode(), hashlib.sha256).digest()
    expected_text = base64.urlsafe_b64encode(expected).decode().rstrip("=")
    return hmac.compare_digest(received.encode(), expected_text.encode())


token = sign("giulia_88:spettatore")
print("token:", token)
print("integro:", verify(token))

body, _, signature = token.partition(".")
forged = base64.urlsafe_b64encode(b"giulia_88:admin").decode().rstrip("=") + "." + signature
print("payload cambiato, firma vecchia:", verify(forged))
print("il payload si legge senza chiave:", base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)).decode())
