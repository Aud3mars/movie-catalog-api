from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Movie


def get_movies(
    db: Session,
    q: str | None = None,
    genre: str | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    sort_by: str = "id",
    order: str = "asc",
    skip: int = 0,
    limit: int = 100,
) -> list[Movie]:
    query = select(Movie)

    if min_year is not None:
        query = query.where(Movie.release_year >= min_year)
    if max_year is not None:
        query = query.where(Movie.release_year <= max_year)
    if min_rating is not None:
        query = query.where(Movie.rating >= min_rating)
    if max_rating is not None:
        query = query.where(Movie.rating <= max_rating)

    movies = list(db.scalars(query).all())

    if q:
        q_text = q.casefold()
        movies = [
            movie for movie in movies
            if q_text in movie.title.casefold() or q_text in movie.director.casefold()
        ]
    if genre:
        genre_text = genre.casefold()
        movies = [movie for movie in movies if movie.genre.casefold() == genre_text]

    def sort_key(movie: Movie):
        value = getattr(movie, sort_by)
        return value.casefold() if isinstance(value, str) else value

    movies.sort(key=sort_key, reverse=(order == "desc"))
    return movies[skip : skip + limit]


def get_movie(db: Session, movie_id: int) -> Movie | None:
    return db.get(Movie, movie_id)


def create_movie(db: Session, data: dict) -> Movie:
    movie = Movie(**data)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update_movie(db: Session, movie: Movie, data: dict) -> Movie:
    for name, value in data.items():
        setattr(movie, name, value)
    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie: Movie) -> None:
    db.delete(movie)
    db.commit()
