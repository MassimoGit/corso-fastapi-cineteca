# Cambiare i parametri senza far reimpostare le password: verify_and_update. File dimostrativo.
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

# I parametri minimi indicati da OWASP: 19 MiB di memoria, 2 iterazioni, 1 thread
old = PasswordHash((Argon2Hasher(memory_cost=19456, time_cost=2, parallelism=1),))
# I parametri di oggi: quelli predefiniti della libreria, più costosi
current = PasswordHash((Argon2Hasher(),))

stored = old.hash("juventus")  # l'hash che c'è nel database da un anno
print("nel database:", stored)

valid, new_hash = current.verify_and_update("juventus", stored)
print("password giusta:", valid, "- nuovo hash da salvare:", new_hash is not None)
print("nuovo hash:", new_hash)

valid, new_hash = current.verify_and_update("juventus", new_hash)
print("al login dopo:", valid, "- nuovo hash:", new_hash)

print("password sbagliata:", current.verify_and_update("sbagliata", stored))
