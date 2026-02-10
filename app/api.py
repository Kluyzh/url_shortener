import logging
from sqlite3 import Connection

from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from app.crud import url_crud
from app.db import get_db_connection
from app.logger import setup_logging
from app.schemas import URLCreate, URLShortenResponse

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/{short_code}')
async def get_url(
        short_code: str,
        conn: Connection = Depends(get_db_connection)
):
    original_url = await url_crud.get_url(short_code, conn)
    logger.info(f'Redirecting {short_code} -> {original_url}')
    return RedirectResponse(
        url=original_url,
        status_code=status.HTTP_302_FOUND
    )


@router.post(
    '/shorten',
    response_model=URLShortenResponse,
    status_code=status.HTTP_201_CREATED
)
async def shorten_url(
        obj_in: URLCreate,
        conn: Connection = Depends(get_db_connection)
):
    return await url_crud.create_url(obj_in, conn)
