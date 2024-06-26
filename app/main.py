import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы запросов
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Функция добавляет хэдер с временем ответа"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
