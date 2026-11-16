"""Le fixture comuni dei test: lo schema di prova, la Session dentro una transaction annullata, il client."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.database import Settings, get_settings, settings
from app.dependencies import get_session
from app.main import app
from app.models import Actor, Base, Director, Movie, MovieActor, Review, Room, Spectator

TEST_SCHEMA = "cineteca_test"
TEST_API_KEY = "test-admin-key"  # la chiave di amministrazione dei test: non è quella del .env


@pytest.fixture
def movie_data() -> dict:
    """Il corpo di un film valido: i test lo modificano solo dove serve."""
    return {
        "title": "La città incantata",
        "director_id": 1,
        "release_year": 2001,
        "runtime_min": 125,
        "purchase_price_eur": 950,
    }


def fill_test_schema(session: Session) -> None:
    """I dati di partenza: pochi, e gli id (da 1) sono quelli che i test scrivono nei percorsi."""
    nolan = Director(name="Christopher Nolan")
    leone = Director(name="Sergio Leone")
    interstellar = Movie(title="Interstellar", director=nolan, release_year=2014, runtime_min=169, purchase_price_eur=1200)
    inception = Movie(title="Inception", director=nolan, release_year=2010, runtime_min=148, purchase_price_eur=1100)
    buono = Movie(
        title="Il buono, il brutto, il cattivo", director=leone, release_year=1966, runtime_min=178, purchase_price_eur=650
    )
    mcconaughey = Actor(name="Matthew McConaughey")
    eastwood = Actor(name="Clint Eastwood")
    session.add_all([
        interstellar,
        inception,
        buono,
        MovieActor(movie=interstellar, actor=mcconaughey, character_name="Joseph Cooper"),
        MovieActor(movie=buono, actor=eastwood, character_name="il Biondo"),
        Room(code="S1", name="Sala Fellini", seats=120),
        Room(code="S2", name="Sala Leone", seats=60),
        Spectator(name="giulia_88", token="giulia-test-token"),
        Spectator(name="marco_cine", token="marco-test-token"),
    ])
    session.flush()  # i film hanno gli id: ora si può scrivere la recensione
    session.add(
        Review(movie_id=interstellar.movie_id, author="giulia_88", rating=5, text="Una storia che commuove.", has_spoilers=False)
    )
    session.commit()


@pytest.fixture(scope="session")
def engine():
    """L'engine dei test. Lo schema cineteca_test nasce qui, con i dati di partenza, e muore a fine sessione."""
    # schema_translate_map: ogni tabella che i model mettono in "cineteca" finisce in "cineteca_test"
    test_engine = create_engine(settings.database_url.get_secret_value()).execution_options(
        schema_translate_map={"cineteca": TEST_SCHEMA}
    )
    with test_engine.begin() as connection:
        connection.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
        connection.execute(text(f"CREATE SCHEMA {TEST_SCHEMA}"))
        Base.metadata.create_all(connection)
    with Session(test_engine) as session:
        fill_test_schema(session)
    yield test_engine
    with test_engine.begin() as connection:
        connection.execute(text(f"DROP SCHEMA {TEST_SCHEMA} CASCADE"))
    test_engine.dispose()


@pytest.fixture
def session(engine):
    """Una Session per test, dentro una transaction che alla fine viene annullata."""
    connection = engine.connect()
    transaction = connection.begin()
    # create_savepoint: il commit() della route chiude un savepoint, non la transaction esterna
    test_session = Session(bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False)
    yield test_session
    test_session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_settings() -> Settings:
    """Le Settings dei test: la chiave di amministrazione è quella scelta qui, non quella del .env."""
    return Settings(admin_api_key=TEST_API_KEY)


@pytest.fixture
def client(session, test_settings):
    """Il TestClient dell'app, con la Session e le Settings dei test al posto di quelle vere."""

    def override_get_session():
        try:
            yield session
        finally:
            session.rollback()  # come la chiusura della Session vera: annulla quello che non è stato committato

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def admin_client(client):
    """Lo stesso app e gli stessi override di client, ma ogni richiesta porta la chiave di amministrazione."""
    return TestClient(app, headers={"X-API-Key": TEST_API_KEY})
