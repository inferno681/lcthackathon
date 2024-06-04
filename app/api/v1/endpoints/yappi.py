from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.models import Yappi
from app.schemas import YappiBase


router = APIRouter()


@router.post(
    '/add'
)
async def add_video(
    data: YappiBase,
    session: AsyncSession = Depends(get_async_session),
):
    new_video = Yappi(**data.dict())
    session.merge(new_video)
    await session.commit()
    result = await session.execute(
        select(Yappi).filter_by(link=new_video.link))
    obj = result.scalars().first()
    return obj
