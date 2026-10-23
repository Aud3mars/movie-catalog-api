from fastapi import FastAPI

from src.routers.movies import router as movies_router

app = FastAPI(
    title="Movie Catalog API",
    description="Учебный backend-проект: каталог фильмов на FastAPI и SQLite",
    version="1.0.0",
)


@app.get("/", tags=["Главная"])
def root():
    return {"message": "Каталог фильмов готов к работе", "docs": "/docs"}


app.include_router(movies_router)
