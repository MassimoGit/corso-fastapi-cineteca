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
    # Il pool di connessioni: quante tenerne aperte, quante in più concedere, quanto aspettare, se verificarle
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: float = 30
    pool_pre_ping: bool = True
    app_name: str = "Cineteca API"
    app_version: str = "0.10.0"
    # La chiave di amministrazione: nel .env, mai nel codice. SecretStr non la fa comparire nei print e nei log.
    admin_api_key: SecretStr


settings = Settings()

engine = create_engine(
    settings.database_url.get_secret_value(),
    echo=settings.echo_sql,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
    pool_timeout=settings.pool_timeout,
    pool_pre_ping=settings.pool_pre_ping,
)


def get_settings() -> Settings:
    """Le Settings dell'app: la funzione che le routes dichiarano come dependency."""
    return settings
