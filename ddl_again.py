"""create_all una seconda volta sullo schema di prova: le tabelle esistono già, non succede niente."""
from app.database import engine
from app.models import Base

DEMO_SCHEMA = "cineteca_ddl_demo"

demo_engine = engine.execution_options(schema_translate_map={"cineteca": DEMO_SCHEMA})

Base.metadata.create_all(demo_engine)
