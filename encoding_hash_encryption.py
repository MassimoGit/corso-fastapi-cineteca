# Tre cose diverse: encoding (base64), hash (sha256), cifratura (AES). File dimostrativo.
import base64
import hashlib
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

message = "giulia_88:ruolo=spettatore"

# 1. Encoding: nessun segreto, chiunque lo riporta com'era
encoded = base64.b64encode(message.encode())
print("base64:", encoded.decode())
print("decodificato da chiunque:", base64.b64decode(encoded).decode())

# 2. Hash: stessa impronta per lo stesso testo, ma dall'impronta non si torna indietro
digest = hashlib.sha256(message.encode()).hexdigest()
print("sha256:", digest)
print("lunghezza:", len(digest), "caratteri, anche per un testo di un milione di caratteri:",
      len(hashlib.sha256(b"x" * 1_000_000).hexdigest()))
print("una lettera diversa:", hashlib.sha256(b"giulia_89:ruolo=spettatore").hexdigest())

# 3. Cifratura: si decifra, ma solo con la chiave
key = AESGCM.generate_key(bit_length=256)  # 32 byte casuali: il segreto
nonce = os.urandom(12)  # numero usato una volta sola per messaggio
ciphertext = AESGCM(key).encrypt(nonce, message.encode(), None)
print("cifrato:", ciphertext.hex())
print("decifrato con la chiave:", AESGCM(key).decrypt(nonce, ciphertext, None).decode())
try:
    AESGCM(AESGCM.generate_key(bit_length=256)).decrypt(nonce, ciphertext, None)
except InvalidTag:
    print("con un'altra chiave: InvalidTag")
