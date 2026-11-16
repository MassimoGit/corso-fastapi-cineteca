"""pool_pre_ping: cosa succede quando il pool conserva una connessione che il server ha chiuso."""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.database import settings

URL = settings.database_url.get_secret_value()
admin = create_engine(URL)  # una seconda engine, che gioca il ruolo del server che chiude le connessioni


def attempt(pre_ping: bool) -> None:
    engine = create_engine(URL, pool_size=1, pool_pre_ping=pre_ping)
    with Session(engine) as session:
        pid = session.scalar(text("SELECT pg_backend_pid()"))  # la connessione resta aperta nel pool

    # Il server chiude la connessione, come farebbe un riavvio del database
    with admin.connect() as connection:
        connection.execute(text("SELECT pg_terminate_backend(:pid)"), {"pid": pid})

    with Session(engine) as session:
        try:
            print(f"pool_pre_ping={pre_ping}: la richiesta risponde", session.scalar(text("SELECT 1")))
        except OperationalError as error:
            print(f"pool_pre_ping={pre_ping}: {type(error).__name__}")
            print(str(error).splitlines()[0])
    engine.dispose()


attempt(False)
attempt(True)
admin.dispose()
