"""Smonta un URL di connessione nei suoi pezzi, senza collegarsi a niente."""
from sqlalchemy import make_url

url = make_url("postgresql+psycopg://mario_rossi:LA_TUA_PASSWORD@pg.abacons.net:5432/mario_rossi?sslmode=require")

print("drivername:", url.drivername)
print("username:", url.username)
print("host:", url.host)
print("port:", url.port)
print("database:", url.database)
print("query:", dict(url.query))
print("url stampato:", url)
