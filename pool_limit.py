"""Il pool di connessioni: pool_size, max_overflow e pool_timeout, con un pool piccolo per vedere il limite."""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import TimeoutError
from sqlalchemy.orm import Session

from app.database import settings

engine = create_engine(
    settings.database_url.get_secret_value(),
    pool_size=2,  # connessioni tenute aperte nel pool
    max_overflow=1,  # connessioni in più concesse nei momenti di punta
    pool_timeout=2,  # secondi di attesa prima di rinunciare
)

sessions = []
for number in range(1, 4):
    session = Session(engine)
    session.execute(text("SELECT 1"))  # la connessione viene presa dal pool alla prima query
    sessions.append(session)
    print(f"richiesta {number} in corso: {engine.pool.checkedout()} connessioni in uso")

try:
    with Session(engine) as fourth:
        fourth.execute(text("SELECT 1"))
except TimeoutError as error:
    print("richiesta 4:", type(error).__name__)
    print(error)

sessions[0].close()  # una richiesta finisce: la connessione torna al pool
with Session(engine) as fourth:
    fourth.execute(text("SELECT 1"))
    print("richiesta 4, dopo che la 1 è finita: ok")

for session in sessions[1:]:
    session.close()
print(f"tutte finite: {engine.pool.checkedout()} in uso, {engine.pool.checkedin()} tenute aperte nel pool")
engine.dispose()
