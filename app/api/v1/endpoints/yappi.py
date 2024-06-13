import os

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import select, or_, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from arq import create_pool
from arq.connections import RedisSettings
from app.core import (
    convert_text_to_embeddings,
    get_async_session,
    parse_tags,
    remove_tags
)
from app.models import Tag, Yappi
from app.schemas import YappiBase

REDIS_SETTINGS = RedisSettings()
router = APIRouter()

UPLOAD_DIRECTORY = "./media"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


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
    '/search_tags',
    response_model=list[YappiBase]
)
async def search_tags(
    q: str = "",
    session: AsyncSession = Depends(get_async_session),
):
    if not q:
        return None
    elif '#' in q:
        tags = parse_tags(q)
        filters = [Tag.name.ilike(f"{tag}%") for tag in tags]
        query = select(Yappi).join(Yappi.tags).where(or_(*filters))
        result = await session.execute(
            query.options(selectinload(Yappi.tags)).limit(1500)
        )
        term = remove_tags(q)
        if term:
            ids = [yappi.id for yappi in result]
            result = await session.execute(
                select(
                    Yappi.tags_description,
                    func.similarity(Yappi.tags_description, term),
                ).where(
                    and_(
                        Yappi.id.in_(ids),
                        Yappi.tags_description.bool_op('%')(term),
                    )).order_by(
                    func.similarity(Yappi.tags_description, term).desc(),
                ).limit(10)
            )
    else:
        term = q
        result = await session.execute(
            select(
                Yappi.tags_description,
                func.similarity(Yappi.tags_description, term),
            ).where(
                Yappi.tags_description.bool_op('%')(term),
            ).order_by(
                func.similarity(Yappi.tags_description, term).desc(),
            ).limit(10)
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


@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        return {"result": "Uploaded"}
    except Exception as e:
        return {"error": str(e)}
