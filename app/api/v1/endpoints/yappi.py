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
    new_video = Yappi(**data.model_dump())
    db_obj = await session.execute(select(Yappi).where(
        Yappi.link == new_video.link))
    instance = db_obj.scalars().one_or_none()
    if instance:
        return instance
    else:
        session.add(new_video)
        await session.commit()
        await session.refresh(new_video)
        return new_video
