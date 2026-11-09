"""Chiama un'app con il TestClient, senza server: python run_client.py modulo METODO /percorso [header=valore]"""
import importlib
import json
import sys

from fastapi.testclient import TestClient

module, method, path, *headers = sys.argv[1:]
client = TestClient(importlib.import_module(module).app, follow_redirects=False)
response = client.request(method, path, headers=dict(h.split("=", 1) for h in headers))
print(f"{method} {path} -> {response.status_code}" + (f" location={response.headers['location']}" if "location" in response.headers else ""))
if response.content:
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
