# == contro compare_digest: il tempo dipende da dove le due chiavi differiscono? File dimostrativo.
import hmac
import time

LENGTH = 50_000_000  # chiavi enormi, apposta: così la differenza si misura
secret = b"a" * LENGTH
wrong_at_start = b"b" + b"a" * (LENGTH - 1)
wrong_at_end = b"a" * (LENGTH - 1) + b"b"


def best_of(function, *args, repeats=7):
    """Il tempo migliore su alcune ripetizioni, in millisecondi."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(*args)
        times.append(time.perf_counter() - start)
    return min(times) * 1000


for name, compare in (("==", lambda a, b: a == b), ("compare_digest", hmac.compare_digest)):
    print(f"{name}: sbagliata alla prima lettera {best_of(compare, secret, wrong_at_start):.4f} ms, "
          f"sbagliata all'ultima {best_of(compare, secret, wrong_at_end):.4f} ms")
