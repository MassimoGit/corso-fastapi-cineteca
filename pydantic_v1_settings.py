"""Pydantic v1: BaseSettings stava dentro pydantic. Oggi non più."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
