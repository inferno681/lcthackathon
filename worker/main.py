from datetime import datetime, timedelta

from arq import Retry
from arq.connections import RedisSettings
from config import config
from db import get_async_session
from ml import video_processing
from models import Embedding, Yappi
from services import check_and_add_tags, parse_tags
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError


REDIS_SETTINGS = RedisSettings(host=config.REDIS_HOST, port=config.REDIS_PORT)


async def add_video_task(ctx: dict, data: dict):
    """Задача на обработку видео"""
    obj = Yappi(**data)
    async for session in get_async_session():
        existing_yappi = await session.execute(select(Yappi).filter_by(link=obj.link))
        if existing_yappi.scalars().first():
            return "in database"
    response = await video_processing(obj.link)
    obj.__dict__.update(response)

    async for session in get_async_session():
        try:
            tags = await check_and_add_tags(
                session, parse_tags(obj.tags_description)
            )
            if tags:
                obj.tags = tags
            embeddings = response.get("embedding")
            if embeddings:
                for emb_value in embeddings:
                    embedding = Embedding(embedding=emb_value, yappi=obj)
                    session.add(embedding)
            session.add(obj)
            await session.commit()
        except IntegrityError:
            return print("in base")
        except Exception as e:
            print(e)
            raise Retry(defer=ctx["job_try"] * 5)
    return "imported"


class WorkerSettings:
    functions = [add_video_task]
    redis_settings = REDIS_SETTINGS
    max_jobs = config.MAX_JOBS
