import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.config import settings
from app.db import init_db

from app.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация."""
    init_db()
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(router)
