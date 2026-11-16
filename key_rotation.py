# Rotazione di una chiave: per un po' valgono la nuova e la vecchia. File dimostrativo.
import secrets

# Nel progetto vero stanno nel .env e in Settings come SecretStr: qui valori di prova
CURRENT_KEY = "chiave-nuova-2026-11"
PREVIOUS_KEY = "chiave-vecchia-2026-05"  # da togliere quando tutti i client hanno la nuova


def is_valid(received: str) -> bool:
    # Si controllano sempre tutte e due, senza fermarsi alla prima: il tempo non dice quale è stata riconosciuta
    valid_keys = [key for key in (CURRENT_KEY, PREVIOUS_KEY) if key]  # una chiave vuota non apre niente
    results = [secrets.compare_digest(received.encode(), key.encode()) for key in valid_keys]
    return any(results)


for received in ("chiave-nuova-2026-11", "chiave-vecchia-2026-05", "chiave-sbagliata"):
    print(f"{received}: {is_valid(received)}")

PREVIOUS_KEY = ""  # a rotazione finita: la vecchia chiave non apre più niente
print("dopo la rotazione, chiave-vecchia-2026-05:", is_valid("chiave-vecchia-2026-05"), "- chiave vuota:", is_valid(""))
