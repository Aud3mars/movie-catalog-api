# Каталог фильмов

## 1. О проекте
Небольшое API для хранения и поиска фильмов.

## 2. Возможности
Добавление, просмотр, изменение и удаление фильмов. Есть поиск, фильтры и сортировка.

## 3. Технологии
Python, FastAPI, SQLAlchemy, SQLite, Alembic, Pydantic, Pytest, Uvicorn.

## 4. Структура проекта
- `src/main.py` — запуск приложения.
- `src/models.py`, `src/schemas.py`, `src/database.py` — данные и работа с БД.
- `src/routers/`, `src/repositories/` — запросы и логика.
- `src/migrations/` — миграции Alembic.
- `tests/` — тесты.
- `requirements.txt`, `alembic.ini`, `pytest.ini` — настройки.

## 5. Быстрый старт
Нужен Python 3.10+.

```powershell
git clone https://github.com/Aud3mars/movie-catalog-api.git
cd movie-catalog-api
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

Документация API: http://127.0.0.1:8000/docs

## 6. Основные эндпоинты
- `GET /movies/` — список фильмов.
- `POST /movies/` — добавить фильм.
- `GET /movies/{movie_id}` — получить фильм.
- `PUT /movies/{movie_id}` — заменить данные.
- `PATCH /movies/{movie_id}` — изменить часть данных.
- `DELETE /movies/{movie_id}` — удалить фильм.

## 7. Фильтры и сортировка
В `GET /movies/` доступны `q` (название или режиссёр), `genre`, `min_year`, `max_year`, `min_rating`, `max_rating`. Сортировка задаётся через `sort_by` (`id`, `title`, `release_year`, `rating`) и `order` (`asc`, `desc`). Для постраничного вывода используются `skip` и `limit`.

Пример: `GET /movies/?genre=Фантастика&sort_by=rating&order=desc`

## 8. Модель данных
Таблица `movies`: `id`, `title`, `director`, `genre`, `release_year`, `rating`, `duration_minutes`, `description`.

## 9. Ограничения БД
`id` — первичный ключ. Название и год выхода вместе должны быть уникальны. Год — от 1888 до 2100, рейтинг — от 0 до 10, длительность — больше 0. Описание необязательное, остальные поля обязательны. Для жанра создан индекс.
