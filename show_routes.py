"""Stampa la tabella delle routes che la chiocciola ha riempito."""
from first_app import app

for route in app.routes:
    print(sorted(route.methods), route.path, route.name)
