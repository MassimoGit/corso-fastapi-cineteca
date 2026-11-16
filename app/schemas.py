"""Gli schemi Pydantic della cineteca: quello che entra e quello che esce dall'API."""
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator, model_validator


def tidy_title(value: str) -> str:
    """Toglie gli spazi in eccesso dentro il titolo e rifiuta un titolo vuoto."""
    cleaned = " ".join(value.split())
    if not cleaned:
        raise ValueError("title cannot be blank")
    return cleaned


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room_id: int
    code: str
    name: str
    seats: int
    is_accessible: bool


class MovieBase(BaseModel):
    """I campi che un film ha sia quando entra sia quando esce."""

    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    director_id: int = Field(ge=1)
    release_year: int = Field(ge=1888, le=2100)
    runtime_min: int = Field(ge=1, le=600)
    plot: str | None = Field(default=None, max_length=2000)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        return tidy_title(value)


class MovieCreate(MovieBase):
    purchase_price_eur: int = Field(ge=0)


class MovieRead(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    movie_id: int


class MovieUpdate(BaseModel):
    """Tutti i campi di MovieCreate, ma nessuno obbligatorio: serve al PATCH."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=200)
    director_id: int | None = Field(default=None, ge=1)
    release_year: int | None = Field(default=None, ge=1888, le=2100)
    runtime_min: int | None = Field(default=None, ge=1, le=600)
    purchase_price_eur: int | None = Field(default=None, ge=0)
    plot: str | None = Field(default=None, max_length=2000)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str | None) -> str | None:
        # Il validator vede anche un "title": null esplicito.
        return value if value is None else tidy_title(value)

    @model_validator(mode="after")
    def reject_null_fields(self):
        # Solo plot può essere azzerato: per gli altri campi null non ha senso.
        for name in self.model_fields_set:
            if name != "plot" and getattr(self, name) is None:
                raise ValueError(f"{name} cannot be null")
        return self


class ReviewCreate(BaseModel):
    """Il corpo di una recensione: l'autore non c'è, lo dice il token dell'header Authorization."""

    # Gli spazi ai bordi si tolgono prima di contare i caratteri: dieci spazi non sono una recensione
    model_config = ConfigDict(str_strip_whitespace=True)

    rating: int = Field(ge=1, le=5)
    text: str = Field(min_length=10, max_length=500)
    has_spoilers: bool = False


class ReviewRead(ReviewCreate):
    model_config = ConfigDict(from_attributes=True)

    review_id: int
    movie_id: int
    author: str


class SpectatorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=20)


class SpectatorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    spectator_id: int
    name: str


class SpectatorCard(SpectatorRead):
    """La risposta alla registrazione: l'unica volta in cui il token esce dall'API."""

    token: str


class UserCreate(BaseModel):
    """Dati di registrazione: niente campo role (mass assignment) e password protetta da SecretStr."""

    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=50)
    password: SecretStr = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    """Risposta pubblica di un utente: mai la password né il suo hash."""

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    role: str


class Token(BaseModel):
    """Risposta standard del endpoint /token per il Bearer token."""

    access_token: str
    token_type: str = "bearer"


class DirectorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    director_id: int
    name: str


class DirectorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ActorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    actor_id: int
    name: str


# Schemi per le righe delle query: i nomi dei campi sono le etichette (label) scelte nella query,
# e non devono essere per forza colonne di un model.
class CatalogueRow(BaseModel):
    movie_id: int
    title: str
    release_year: int
    director_name: str


class CastMember(BaseModel):
    actor: str
    character: str


class DirectorStats(BaseModel):
    director: str
    movies: int


# Schemi annidati costruiti dalle relationship: il film con il suo regista e il suo cast.
class CastRole(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    character_name: str
    actor: ActorRead


class MovieDetail(MovieRead):
    director: DirectorRead
    cast: list[CastRole]
