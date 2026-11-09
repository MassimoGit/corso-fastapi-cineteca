"""Connessione al database della cineteca, configurata dalle Settings lette dal file .env."""
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine

BASE = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE / ".env", extra="ignore")

    database_url: SecretStr
    echo_sql: bool = False
    app_name: str = "Cineteca API"
    app_version: str = "0.5.0"


settings = Settings()
engine = create_engine(settings.database_url.get_secret_value(), echo=settings.echo_sql)
