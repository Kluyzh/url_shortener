import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.db import get_db_connection
from app.main import app


@pytest.fixture()
def test_db():
    """Создание временной in-memory базы данных для тестов."""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_code TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE INDEX idx_short_code ON urls(short_code)
    """)

    conn.commit()

    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture()
def override_get_db_connection(test_db):
    """Переопределение get_db_connection для использования тестовой БД."""

    def _override_get_db_connection():
        return test_db

    return _override_get_db_connection


@pytest.fixture()
def test_client(override_get_db_connection):
    """Создание тестового клиента с переопределенной зависимостью БД."""
    app.dependency_overrides[get_db_connection] = override_get_db_connection

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_create_short_url_success(test_client):
    """Тест: Проверка что создается успешно короткая ссылка."""
    test_url = 'https://example.com/test-page'

    response = test_client.post('/shorten', json={'url': test_url})

    assert response.status_code == 201, (
        f'Ожидался 201, получен {response.status_code}'
    )
    data = response.json()
    assert data['original_url'] == test_url, 'Оригинальный URL не совпадает'

    assert 'short_link' in data, 'В ответе нет short_link'
    assert data['short_link'].startswith(settings.base_url), (
        'Короткая ссылка должна начинаться с базового URL'
    )


def test_create_duplicate_url_returns_existing(test_client, test_db):
    """
    Тест: Если такая ссылка существует в базе,
    то возвращается та же самая короткая ссылка.
    """
    test_url = 'https://example.com/duplicate-test'

    response1 = test_client.post('/shorten', json={'url': test_url})
    assert response1.status_code == 201, 'Первый запрос должен быть успешным'

    data1 = response1.json()
    first_short_link = data1['short_link']

    response2 = test_client.post('/shorten', json={'url': test_url})
    assert response2.status_code == 201, (
        'Второй запрос также должен быть успешным'
    )

    data2 = response2.json()

    assert data2['short_link'] == first_short_link, (
        'Должен возвращаться тот же короткий URL'
    )
    cursor = test_db.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM urls WHERE original_url = ?', (test_url,)
    )
    count = cursor.fetchone()[0]
    assert count == 1, (
        f'В базе должна быть 1 запись для этого URL, но найдено {count}'
    )


def test_get_redirect_works_successfully(test_client, test_db):
    """Тест: Проверка что успешно работает get запрос."""
    test_url = 'https://example.com/redirect-target'

    shorten_response = test_client.post('/shorten', json={'url': test_url})
    assert shorten_response.status_code == 201, (
        'Создание короткой ссылки должно быть успешным'
    )
    data = shorten_response.json()
    short_link = data['short_link']

    redirect_response = test_client.get(
        short_link, follow_redirects=False
    )
    assert redirect_response.status_code == 302, (
        f'Ожидался 302, получен {redirect_response.status_code}'
    )
