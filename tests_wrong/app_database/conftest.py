"""Solo dimostrativo. Al posto del database vero (lo schema cineteca) c'è uno schema d'appoggio, cineteca_test:
le routes dell'app lo usano con la loro get_session, e quello che scrivono resta lì anche dopo i test."""
import pytest
from sqlalchemy import create_engine, text

from app import dependencies
from app.database import settings
from app.models import Base


@pytest.fixture(scope="session", autouse=True)
def database_of_the_app():
    stand_in = create_engine(settings.database_url.get_secret_value()).execution_options(
        schema_translate_map={"cineteca": "cineteca_test"}
    )
    with stand_in.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS cineteca_test"))
        Base.metadata.create_all(connection)
    original = dependencies.engine
    dependencies.engine = stand_in  # get_session legge questo nome: da qui in poi l'app scrive nello schema d'appoggio
    yield
    dependencies.engine = original
    stand_in.dispose()
