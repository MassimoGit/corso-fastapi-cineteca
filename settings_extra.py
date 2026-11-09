"""Errore comune: il .env contiene una variabile che le Settings non dichiarano."""
import tempfile
from pathlib import Path

from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

with tempfile.TemporaryDirectory() as folder:
    # Un .env di prova, in una cartella temporanea che sparisce alla fine.
    env_file = Path(folder) / ".env"
    env_file.write_text("DATABASE_URL=postgresql+psycopg://utente:password@localhost/db\nECHO_SQL=true\n", encoding="utf-8")

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(env_file=env_file)

        database_url: SecretStr

    try:
        Settings()
    except ValidationError as error:
        print(error.errors()[0]["loc"], error.errors()[0]["type"], "|", error.errors()[0]["msg"])
