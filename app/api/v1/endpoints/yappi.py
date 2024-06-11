from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from arq import create_pool
from arq.connections import RedisSettings
from app.core import get_async_session
from app.models import Yappi
from app.schemas import YappiBase
from app.ml import convert_text_to_embeddings, add_video as add

REDIS_SETTINGS = RedisSettings()
router = APIRouter()


@router.post(
    '/add',
    response_model=YappiBase
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
        res = await add(new_video.link)
        new_video.__dict__.update(res)
        session.add(new_video)
        await session.commit()
        await session.refresh(new_video)
        return new_video


@router.post(
    '/add_queue',
    response_model=YappiBase
)
async def add_video_arq(
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
        redis = await create_pool(REDIS_SETTINGS)
        await redis.enqueue_job('add_video_task', new_video)
        return new_video


@router.get(
    '/search_usual',
    response_model=list[YappiBase]
)
async def search_usual(
    q: str = "",
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(Yappi).where(Yappi.tags_description.ilike(f"{q}%"))
    )
    videos = result.scalars().all()
    return [YappiBase.model_validate(video) for video in videos]


@router.get(
    '/search',
    response_model=list[YappiBase]
)
async def search_video(
    q: str = "",
    session: AsyncSession = Depends(get_async_session),
):
    vector = await convert_text_to_embeddings(q)
    result = await session.scalars(select(Yappi).order_by(
        Yappi.embedding_description.l2_distance(vector)
    ).limit(5))

    return [YappiBase.model_validate(video) for video in result]
