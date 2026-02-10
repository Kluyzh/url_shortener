import logging
from sqlite3 import Connection

from fastapi import HTTPException, status

from app.config import settings
from app.schemas import URLCreate, URLShortenResponse
from app.utils import generate_short_code

logger = logging.getLogger(__name__)


class URLCRUD:
    async def get_url(short_code: str, conn: Connection):
        cursor = conn.cursor()
        cursor.execute(
            'SELECT original_url FROM urls WHERE short_code = ?',
            (short_code,)
        )
        result = cursor.fetchone()
        if not result:
            logger.warning(f'Short code {short_code} was not found')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Short URL was not found'
            )
        original_url = result[0]
        return original_url

    async def create_url(obj_in: URLCreate, conn: Connection):
        original_url = obj_in.url
        short_code = generate_short_code()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO urls (original_url, short_code) VALUES (?, ?)',
                (original_url, short_code)
            )
        except Exception as e:
            logger.error(f'Database error: {e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Internal server error'
            )
        short_link = f'{settings.base_url}/{short_code}'
        logger.info(f'URL shortened: {original_url} -> {short_link}')
        return URLShortenResponse(
            original_url=original_url,
            short_link=short_link
        )


url_crud = URLCRUD()
