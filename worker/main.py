import os

from arq import Retry
from arq.connections import RedisSettings
from config import config
from db import get_async_session
from ml import video_processing
from models import Yappi
from services import check_and_add_tags, parse_tags, send_file_to_fastapi


REDIS_SETTINGS = RedisSettings(host=config.REDIS_HOST, port=config.REDIS_PORT)


async def add_video_task(ctx: dict, data: dict):
    """Задача на обработку видео"""
    obj = Yappi(**data)
    response = await video_processing(obj.link)
    obj.__dict__.update(response)

    async for session in get_async_session():
        try:
            tags = await check_and_add_tags(
                session, parse_tags(obj.tags_description)
            )
            obj.tags = tags
            obj.embeddings = response["embedding"]
            session.add(obj)
            await session.commit()
        except Exception:
            raise Retry(defer=ctx["job_try"] * 5)
        await send_file_to_fastapi(
            response["face"], config.SCREENSHOT_UPLOAD_LINK
        )
        os.remove(response["face"])
    return "imported"


class WorkerSettings:
    functions = [add_video_task]
    redis_settings = REDIS_SETTINGS
