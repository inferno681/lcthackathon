from arq.connections import RedisSettings
from .config import config
from .db import check_and_add_tags, get_async_session, parse_tags
from .ml import add_video
from .services import check_and_add_tags, parse_tags


REDIS_SETTINGS = RedisSettings(host=config.REDIS_PORT, port=config.REDIS_PORT)


async def add_video_task(ctx, obj):

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
    return 'imported'


class WorkerSettings:
    functions = [add_video_task]
    redis_settings = REDIS_SETTINGS
