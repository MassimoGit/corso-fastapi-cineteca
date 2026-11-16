# Quanti bit ha un segreto e quanto costa indovinarlo. File dimostrativo.
import math
import random
import secrets
import string

GUESSES_PER_SECOND = 10_000_000_000  # ipotesi: un attaccante con una scheda grafica, contro un hash veloce
SECONDS_PER_YEAR = 365 * 24 * 3600



def readable(seconds):
    """Il tempo nell'unità più comoda da leggere."""
    for unit, size in (("anni", SECONDS_PER_YEAR), ("giorni", 86400), ("ore", 3600), ("minuti", 60)):
        if seconds >= size:
            return f"{seconds / size:.3g} {unit}"
    return f"{seconds:.3g} secondi"


secrets_to_compare = {
    "PIN di 4 cifre": 10 ** 4,
    "password di 8 lettere minuscole": 26 ** 8,
    "password di 8 caratteri qualsiasi": len(string.ascii_letters + string.digits + string.punctuation) ** 8,
    "token_urlsafe(16), 128 bit": 2 ** 128,
    "token_urlsafe(32), 256 bit": 2 ** 256,
}
for name, possibilities in secrets_to_compare.items():
    seconds = possibilities / 2 / GUESSES_PER_SECOND  # in media si indovina a meta strada
    print(f"{name}: {math.log2(possibilities):.1f} bit, in media {readable(seconds)}")

print(len(secrets.token_urlsafe(32)), "caratteri per 32 byte, cioè", 32 * 8, "bit")

# random: stesso seme, stessa sequenza. secrets: nessun seme da scoprire
random.seed(2026)
first = [random.randrange(100) for _ in range(5)]
random.seed(2026)
print("random, seme 2026, due volte:", first, [random.randrange(100) for _ in range(5)])
print("secrets, due volte:", [secrets.randbelow(100) for _ in range(5)], [secrets.randbelow(100) for _ in range(5)])
