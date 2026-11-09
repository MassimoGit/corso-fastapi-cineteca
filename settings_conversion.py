"""Un .env dà solo stringhe: os.getenv le lascia tali, Settings le converte."""
import os

from pydantic import ValidationError
from pydantic_settings import BaseSettings


class Flags(BaseSettings):
    echo_sql: bool = False


print(f"{'ECHO_SQL':9}{'bool(getenv)':14}Settings")
for value in ["true", "false", "1", "off", "maybe"]:
    os.environ["ECHO_SQL"] = value
    try:
        converted = Flags().echo_sql
    except ValidationError as error:
        converted = error.errors()[0]["msg"]
    print(f"{value:9}{bool(os.getenv('ECHO_SQL'))!s:14}{converted}")
