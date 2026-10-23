from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_db
from src.repositories import movies_repository
from src.schemas import MovieCreate, MovieOut, MovieUpdate

router = APIRouter(prefix="/movies", tags=["Фильмы"])


def get_movie_or_404(db: Session, movie_id: int):
    movie = movies_repository.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie


def save_or_conflict(db: Session, save_function):
    try:
        return save_function()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Фильм с таким названием и годом уже существует либо нарушено ограничение БД",
        ) from None


@router.get("/", response_model=list[MovieOut])
def list_movies(
    q: str | None = Query(default=None, description="Часть названия фильма или имени режиссёра"),
    genre: str | None = Query(default=None, description="Жанр (без учёта регистра)"),
    min_year: int | None = Query(default=None, ge=1888, le=2100),
    max_year: int | None = Query(default=None, ge=1888, le=2100),
    min_rating: float | None = Query(default=None, ge=0, le=10),
    max_rating: float | None = Query(default=None, ge=0, le=10),
    sort_by: Literal["id", "title", "release_year", "rating"] = "id",
    order: Literal["asc", "desc"] = "asc",
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if min_year is not None and max_year is not None and min_year > max_year:
        raise HTTPException(status_code=422, detail="min_year не должен быть больше max_year")
    if min_rating is not None and max_rating is not None and min_rating > max_rating:
        raise HTTPException(status_code=422, detail="min_rating не должен быть больше max_rating")
    return movies_repository.get_movies(
        db, q, genre, min_year, max_year, min_rating, max_rating, sort_by, order, skip, limit
    )


@router.post("/", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
def add_movie(movie_data: MovieCreate, db: Session = Depends(get_db)):
    return save_or_conflict(
        db, lambda: movies_repository.create_movie(db, movie_data.model_dump())
    )


@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    return get_movie_or_404(db, movie_id)


@router.put("/{movie_id}", response_model=MovieOut)
def replace_movie(movie_id: int, movie_data: MovieCreate, db: Session = Depends(get_db)):
    movie = get_movie_or_404(db, movie_id)
    return save_or_conflict(
        db, lambda: movies_repository.update_movie(db, movie, movie_data.model_dump())
    )


@router.patch("/{movie_id}", response_model=MovieOut)
def edit_movie(movie_id: int, movie_data: MovieUpdate, db: Session = Depends(get_db)):
    movie = get_movie_or_404(db, movie_id)
    return save_or_conflict(
        db,
        lambda: movies_repository.update_movie(
            db, movie, movie_data.model_dump(exclude_unset=True)
        ),
    )


@router.delete("/{movie_id}")
def remove_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = get_movie_or_404(db, movie_id)
    movies_repository.delete_movie(db, movie)
    return {"message": "Фильм удалён"}
