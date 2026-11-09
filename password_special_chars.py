"""Una password con @ o # rompe l'URL scritto a mano; URL.create la protegge."""
from sqlalchemy import URL, create_engine, text

PASSWORD = "pa@ss#word"

# Sbagliato: la password va dentro la stringa così com'è.
broken = f"postgresql+psycopg://mario_rossi:{PASSWORD}@localhost:5432/mario_rossi"
try:
    with create_engine(broken).connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception as error:
    print(type(error).__name__ + ":", str(error).splitlines()[0])

# Giusto: i pezzi si passano separati e SQLAlchemy li codifica.
url = URL.create(
    "postgresql+psycopg",
    username="mario_rossi",
    password=PASSWORD,
    host="localhost",
    port=5432,
    database="mario_rossi",
)
print("stampato:", url)
print("scritto per esteso:", url.render_as_string(hide_password=False))
