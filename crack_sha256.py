# Un hash veloce (sha256) contro un dizionario di password comuni. File dimostrativo.
import hashlib
import time

COMMON_PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon",
    "123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop",
    "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000",
    "ciao1234", "juventus", "napoli", "password1", "iloveyou", "sardegna",
]

# La tabella degli utenti, come l'avrebbe scritta chi salva sha256(password)
users = {
    "giulia_88": hashlib.sha256(b"juventus").hexdigest(),
    "luca_77": hashlib.sha256(b"sardegna").hexdigest(),
    "marta_01": hashlib.sha256(b"cWk9-Zt4_Lm2!x").hexdigest(),  # non è nel dizionario
}


def crack(stored_hash):
    """Prova ogni parola del dizionario: restituisce quella che ha quell'hash, o None."""
    for candidate in COMMON_PASSWORDS:
        if hashlib.sha256(candidate.encode()).hexdigest() == stored_hash:
            return candidate
    return None


start = time.perf_counter()
for name, stored_hash in users.items():
    found = crack(stored_hash)
    print(f"{name}: trovata '{found}'" if found else f"{name}: non è nel dizionario")
elapsed = time.perf_counter() - start
print(f"{len(COMMON_PASSWORDS)} parole x {len(users)} utenti in {elapsed * 1000:.2f} ms")

# Quanti sha256 al secondo fa questo computer, in Python
N = 1_000_000
start = time.perf_counter()
for i in range(N):
    hashlib.sha256(f"password{i}".encode()).digest()
rate = N / (time.perf_counter() - start)
print(f"{rate:,.0f} sha256 al secondo (un solo core, Python)")
print(f"tutte le password di 8 lettere minuscole ({26 ** 8:,}): {26 ** 8 / rate / 3600:.1f} ore su questo computer")
