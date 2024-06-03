import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.core import config

tags_metadata = [
    {"name": "user", "description": "Запросы пользователя"},
]

app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    openapi_tags=tags_metadata,
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
