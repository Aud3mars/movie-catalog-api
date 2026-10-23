from alembic import op
import sqlalchemy as sa

revision = "8b9a4a6e1023"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("director", sa.String(length=120), nullable=False),
        sa.Column("genre", sa.String(length=80), nullable=False),
        sa.Column("release_year", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title", "release_year", name="uq_movies_title_year"),
        sa.CheckConstraint("release_year BETWEEN 1888 AND 2100", name="ck_movies_year_range"),
        sa.CheckConstraint("rating BETWEEN 0 AND 10", name="ck_movies_rating_range"),
        sa.CheckConstraint("duration_minutes > 0", name="ck_movies_duration_positive"),
    )
    op.create_index("ix_movies_genre", "movies", ["genre"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_movies_genre", table_name="movies")
    op.drop_table("movies")
