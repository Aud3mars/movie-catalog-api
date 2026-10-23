from pydantic import BaseModel, ConfigDict, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    director: str = Field(min_length=1, max_length=120)
    genre: str = Field(min_length=1, max_length=80)
    release_year: int = Field(ge=1888, le=2100)
    rating: float = Field(ge=0, le=10)
    duration_minutes: int = Field(gt=0)
    description: str | None = None


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    director: str | None = Field(default=None, min_length=1, max_length=120)
    genre: str | None = Field(default=None, min_length=1, max_length=80)
    release_year: int | None = Field(default=None, ge=1888, le=2100)
    rating: float | None = Field(default=None, ge=0, le=10)
    duration_minutes: int | None = Field(default=None, gt=0)
    description: str | None = None


class MovieOut(MovieCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
