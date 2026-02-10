import logging
import sqlite3

from app.config import settings

from app.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect(settings.database_url)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_code TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_short_code ON urls(short_code)
    """)

    conn.commit()
    conn.close()
    logger.info('Database initialized')


def get_db_connection():
    """Получение соединения с БД."""
    conn = sqlite3.connect(settings.database_url, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()
