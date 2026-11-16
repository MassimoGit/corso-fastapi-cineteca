"""Il client di prova per slow_app.py: quattro richieste a /slow nello stesso momento."""
import time
from concurrent.futures import ThreadPoolExecutor

import requests

URL = "http://127.0.0.1:8000/slow"


def call(number: int) -> str:
    started = time.perf_counter()
    response = requests.get(URL, timeout=30)
    return f"richiesta {number}: {response.status_code} dopo {time.perf_counter() - started:.1f} s"


with ThreadPoolExecutor(max_workers=4) as executor:  # quattro thread, uno per richiesta
    for line in executor.map(call, range(1, 5)):
        print(line)
