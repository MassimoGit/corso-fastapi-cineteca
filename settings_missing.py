"""Una variabile obbligatoria mancante: l'errore arriva subito, all'avvio."""
from pydantic import SecretStr, ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: SecretStr
    echo_sql: bool = False


try:
    Settings()
except ValidationError as error:
    print(error)
