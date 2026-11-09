"""Controlla che il file .env accanto a questo script contenga DATABASE_URL."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

url = os.getenv("DATABASE_URL")
print("DATABASE_URL trovata:", url is not None)
print("è una stringa:", isinstance(url, str))
