import pytest

MOVIE_1 = {
    "title": "Начало",
    "director": "Кристофер Нолан",
    "genre": "Фантастика",
    "release_year": 2010,
    "rating": 8.8,
    "duration_minutes": 148,
    "description": "История о сновидениях",
}
MOVIE_2 = {
    "title": "Интерстеллар",
    "director": "Кристофер Нолан",
    "genre": "Фантастика",
    "release_year": 2014,
    "rating": 8.6,
    "duration_minutes": 169,
}
MOVIE_3 = {
    "title": "1+1",
    "director": "Оливье Накаш",
    "genre": "Комедия",
    "release_year": 2011,
    "rating": 8.4,
    "duration_minutes": 112,
}


def add_movies(client):
    for movie in (MOVIE_1, MOVIE_2, MOVIE_3):
        result = client.post("/movies/", json=movie)
        assert result.status_code == 201


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_create_and_read_movie(client):
    response = client.post("/movies/", json=MOVIE_1)
    assert response.status_code == 201
    movie_id = response.json()["id"]
    assert response.json()["title"] == "Начало"
    assert client.get(f"/movies/{movie_id}").json()["release_year"] == 2010


def test_list_movies(client):
    add_movies(client)
    response = client.get("/movies/")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.parametrize(
    "params, expected_names",
    [
        ({}, ["Начало", "Интерстеллар", "1+1"]),
        ({"q": "интер"}, ["Интерстеллар"]),
        ({"genre": "фантастика"}, ["Начало", "Интерстеллар"]),
        ({"min_year": 2012}, ["Интерстеллар"]),
        ({"min_rating": 8.7}, ["Начало"]),
        ({"max_year": 2011, "min_rating": 8.5}, ["Начало"]),
    ],
)
def test_movie_filters(client, params, expected_names):
    add_movies(client)
    response = client.get("/movies/", params=params)
    assert response.status_code == 200
    assert sorted(movie["title"] for movie in response.json()) == sorted(expected_names)


def test_sort_by_rating_desc(client):
    add_movies(client)
    response = client.get("/movies/", params={"sort_by": "rating", "order": "desc"})
    assert response.status_code == 200
    assert [movie["title"] for movie in response.json()] == ["Начало", "Интерстеллар", "1+1"]


def test_pagination(client):
    add_movies(client)
    response = client.get("/movies/", params={"skip": 1, "limit": 1})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_replace_and_partial_update(client):
    movie_id = client.post("/movies/", json=MOVIE_1).json()["id"]
    new_movie = {**MOVIE_1, "rating": 9.0}
    assert client.put(f"/movies/{movie_id}", json=new_movie).status_code == 200
    response = client.patch(f"/movies/{movie_id}", json={"genre": "Драма"})
    assert response.status_code == 200
    assert response.json()["rating"] == 9.0
    assert response.json()["genre"] == "Драма"


def test_delete_movie(client):
    movie_id = client.post("/movies/", json=MOVIE_1).json()["id"]
    assert client.delete(f"/movies/{movie_id}").status_code == 200
    assert client.get(f"/movies/{movie_id}").status_code == 404


def test_duplicate_is_conflict(client):
    assert client.post("/movies/", json=MOVIE_1).status_code == 201
    assert client.post("/movies/", json=MOVIE_1).status_code == 409


@pytest.mark.parametrize("field,value", [("rating", 10.5), ("release_year", 1800), ("duration_minutes", 0)])
def test_invalid_data(client, field, value):
    invalid_movie = {**MOVIE_1, field: value}
    assert client.post("/movies/", json=invalid_movie).status_code == 422


def test_invalid_filter_range(client):
    response = client.get("/movies/", params={"min_year": 2020, "max_year": 2010})
    assert response.status_code == 422
