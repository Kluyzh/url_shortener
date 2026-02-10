from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    url: HttpUrl


class URLShortenResponse(BaseModel):
    original_url: HttpUrl
    short_link: HttpUrl
