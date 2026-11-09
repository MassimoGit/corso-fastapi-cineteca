"""Le impostazioni dell'app (variabili d'ambiente e .env) e la connessione al database della cineteca."""
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine

# La cartella che contiene app/: il .env sta lì, accanto alla cartella app
BASE = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE / ".env", extra="ignore")

    database_url: SecretStr
    echo_sql: bool = False
    app_name: str = "Cineteca API"
    app_version: str = "0.7.0"
    # Le tessere dei clienti della cineteca: chi può scrivere una recensione
    spectators: list[str] = ["giulia_88", "marco_cine", "anna_film", "luca_77"]


settings = Settings()

engine = create_engine(settings.database_url.get_secret_value(), echo=settings.echo_sql)


def get_settings() -> Settings:
    """Le Settings dell'app: la funzione che le routes dichiarano come dependency."""
    return settings
