from sqlalchemy.ext.asyncio import AsyncSession

from arq.connections import RedisSettings
from app.core.db import AsyncSessionLocal
from app.ml import add_video

# Here you can configure the Redis connection.
# The default is to connect to localhost:6379, no password.
REDIS_SETTINGS = RedisSettings()


async def add_video_task(ctx, obj):
    session: AsyncSession = ctx['session']
    response = await add_video(obj.link)
    obj.__dict__.update(response)
    session.add(obj)
    await session.commit()
    return {'imported'}


async def startup(ctx):
    ctx['session'] = AsyncSessionLocal()


async def shutdown(ctx):
    await ctx['session'].aclose()


# WorkerSettings defines the settings to use when creating the work,
# It's used by the arq CLI.
# redis_settings might be omitted here if using the default settings
# For a list of all available settings, see https://arq-docs.helpmanual.io/#arq.worker.Worker


class WorkerSettings:
    functions = [add_video_task]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = REDIS_SETTINGS
