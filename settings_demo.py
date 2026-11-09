"""Le Settings dell'applicazione lette dal .env: i tipi, e la password che non si stampa."""
from database import settings

print(settings)
print("echo_sql:", settings.echo_sql, type(settings.echo_sql).__name__)
print("database_url:", settings.database_url)
print("tipo:", type(settings.database_url).__name__)
print("il valore vero comincia con 'postgresql+psycopg://':", settings.database_url.get_secret_value().startswith("postgresql+psycopg://"))
