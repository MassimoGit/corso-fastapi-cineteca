# Un segreto che finisce in un log: con str e con SecretStr. File dimostrativo.
import logging
import sys

from pydantic import BaseModel, SecretStr

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="LOG %(levelname)s %(message)s")
logger = logging.getLogger("api")


class LoginWrong(BaseModel):  # SBAGLIATO APPOSTA: la password è una str qualunque
    username: str
    password: str


class Login(BaseModel):
    username: str
    password: SecretStr


wrong = LoginWrong(username="giulia_88", password="juventus")
right = Login(username="giulia_88", password="juventus")

logger.info("tentativo di accesso: %s", wrong)
logger.info("tentativo di accesso: %s", right)
logger.info("tentativo di accesso: %s", right.model_dump())
logger.info("tentativo di accesso: %s", right.model_dump_json())
print("per usarla serve chiederla apposta:", right.password.get_secret_value())
