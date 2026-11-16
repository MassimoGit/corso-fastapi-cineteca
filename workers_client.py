"""Il client di prova per workers_app.py: quattro richieste a /who a un decimo di secondo l'una dall'altra."""
import time
from concurrent.futures import ThreadPoolExecutor

import requests

URL = "http://127.0.0.1:8000/who"


def call(number: int) -> dict:
    time.sleep(number * 0.1)  # partono scaglionate, ma restano tutte in corso insieme
    return requests.get(URL, timeout=30).json()


with ThreadPoolExecutor(max_workers=4) as executor:
    answers = list(executor.map(call, range(4)))

for answer in sorted(answers, key=lambda a: (a["worker"], a["connection"])):  # ordinate, per leggerle meglio
    print(f"worker {answer['worker']}, connessione {answer['connection']}")
