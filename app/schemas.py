from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    """Схема создания."""
    url: HttpUrl


class URLShortenResponse(BaseModel):
    """Схема ответа."""
    original_url: HttpUrl
    short_link: HttpUrl
