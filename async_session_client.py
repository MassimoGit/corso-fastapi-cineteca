"""Lancia una route lenta e, mezzo secondo dopo, /fast: quanto aspetta /fast?"""
import threading
import time

import requests

URL = "http://127.0.0.1:8000"


def timed(path):
    started = time.perf_counter()
    response = requests.get(URL + path, timeout=30)
    return response.status_code, time.perf_counter() - started


for slow in ("/slow-sync", "/slow-async"):
    result = {}
    thread = threading.Thread(target=lambda: result.update(slow=timed(slow)))
    thread.start()
    time.sleep(0.5)
    status, seconds = timed("/fast")
    thread.join()
    print(f"{slow}: /fast risponde {status} dopo {seconds:.1f} s")
