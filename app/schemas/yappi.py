from pydantic import BaseModel


class YappiBase(BaseModel):
    link: str
    deskr_tags: str
