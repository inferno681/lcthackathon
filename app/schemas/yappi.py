from pydantic import BaseModel


class YappiBase(BaseModel):
    link: str
    tags_description: str
