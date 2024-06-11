from arq.connections import RedisSettings
from app.core.db import get_async_session
from app.ml import add_video


REDIS_SETTINGS = RedisSettings()


async def add_video_task(ctx, obj):

    response = await add_video(obj.link)
    obj.__dict__.update(response)
    async for session in get_async_session():
        try:
            session.add(obj)
            await session.commit()
        except Exception as e:
            return e
    return 'imported'


class WorkerSettings:
    functions = [add_video_task]
    redis_settings = REDIS_SETTINGS
