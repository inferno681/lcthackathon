from pydantic import BaseModel


class YappiBase(BaseModel):
    """Базовая схема запроса с ссылкой на видео и описанием"""

    link: str
    tags_description: str

    class Config:
        from_attributes = True
