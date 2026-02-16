from pydantic import BaseModel, ConfigDict

class FilmBase(BaseModel):
    title: str
    director: str
    release_year: int
    genre: str | None = None
    rating: str | None = None

class FilmCreate(FilmBase):
    pass

class FilmReturn(FilmBase):
    film_id: int
    model_config = ConfigDict(from_attributes=True)

class FilmUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    release_year: int | None = None
    genre: str | None = None
    rating: str | None = None