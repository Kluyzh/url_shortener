# URL Shortener API

Сервис для сокращения ссылок на FastAPI.

## Технологии
- Python 3.12+
- FastAPI
- SQLite3 (без ORM)
- Pytest

## Установка и запуск

1. Клонируйте репозиторий

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Запустите приложение:

```bash
uvicorn app.main:app
```

4. API Endpoints:

POST /shorten
Сокращает длинную ссылку.

Request:

```json
{
  "url": "https://example.com/very/long/url"
}
```
Response (201):

```json
{
  "short_link": "http://localhost:8000/abc123",
  "original_url": "https://example.com/very/long/url"
}
```

GET /{short_code}
Перенаправляет на оригинальный URL.

Response:

302 Redirect: успешное перенаправление

404: короткая ссылка не найдена

5. Запуск тестов:
```bash
pytest
```
6. Логирование:
Логи сохраняются в файл url_shortener.log и выводятся в консоль.
