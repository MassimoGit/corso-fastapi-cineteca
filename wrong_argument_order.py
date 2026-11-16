# verify(password, hash) con i due argomenti scambiati. SBAGLIATO APPOSTA.
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

password_hash = PasswordHash.recommended()
stored = password_hash.hash("juventus")

print("giusto, verify(password, hash):", password_hash.verify("juventus", stored))
try:
    password_hash.verify(stored, "juventus")  # SBAGLIATO: prima l'hash, poi la password
except UnknownHashError as error:
    print("UnknownHashError:", error)
