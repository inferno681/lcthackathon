from arq.connections import RedisSettings
from config import config
from db import get_async_session
from ml import add_video
from models import Yappi
from services import check_and_add_tags, parse_tags, send_file_to_fastapi


REDIS_SETTINGS = RedisSettings(host=config.REDIS_HOST, port=config.REDIS_PORT)


async def add_video_task(ctx, data):
    obj = Yappi(**data)
    response = await add_video(obj.link)
    obj.__dict__.update(response)

    async for session in get_async_session():
        try:
            tags = await check_and_add_tags(
                session, parse_tags(obj.tags_description))
            obj.tags = tags
            session.add(obj)
            await session.commit()
        except Exception as e:
            return e
        await send_file_to_fastapi(response['face'], 'http://127.0.0.1:8000/api/v1/upload-image/')
    return 'imported'


class WorkerSettings:
    functions = [add_video_task]
    redis_settings = REDIS_SETTINGS
