from sqlalchemy import CheckConstraint, Column, Float, Index, Integer, String, Text, UniqueConstraint

from src.database import Base


class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint("title", "release_year", name="uq_movies_title_year"),
        CheckConstraint("release_year BETWEEN 1888 AND 2100", name="ck_movies_year_range"),
        CheckConstraint("rating BETWEEN 0 AND 10", name="ck_movies_rating_range"),
        CheckConstraint("duration_minutes > 0", name="ck_movies_duration_positive"),
        Index("ix_movies_genre", "genre"),
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    director = Column(String(120), nullable=False)
    genre = Column(String(80), nullable=False)
    release_year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
