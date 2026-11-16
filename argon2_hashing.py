# Salt e hash lenti: argon2 con pwdlib. File dimostrativo.
import time

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()  # argon2id, parametri predefiniti della libreria

password = "juventus"
first = password_hash.hash(password)
second = password_hash.hash(password)
print(first)
print(second)
print("stesso hash?", first == second)
print("verify giusta:", password_hash.verify(password, first), "- sbagliata:", password_hash.verify("juventu5", first))

start = time.perf_counter()
for _ in range(5):
    password_hash.hash(password)
per_hash = (time.perf_counter() - start) / 5
print(f"un hash argon2: {per_hash * 1000:.0f} ms (sha256: circa un microsecondo)")
print(f"36 parole del dizionario contro un utente: {36 * per_hash:.1f} s")
