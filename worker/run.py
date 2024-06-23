import time
import asyncio
from config import config
from db import get_async_session
from ml import video_processing
from models import Embedding, Yappi
from services import check_and_add_tags, parse_tags
import csv
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


async def add_video_task(data: dict):
    """Задача на обработку видео"""
    obj = Yappi(**data)
    async for session in get_async_session():
        existing_yappi = await session.execute(select(Yappi).filter_by(link=obj.link))
        if existing_yappi.scalars().first():
            return print("in base")
    response = await video_processing(obj.link)
    print(response)
    obj.__dict__.update(response)

    async for session in get_async_session():
        try:
            tags = await check_and_add_tags(
                session, parse_tags(obj.tags_description)
            )
            obj.tags = tags
            embeddings = response["embedding"]
            for emb_value in embeddings:
                embedding = Embedding(embedding=emb_value, yappi=obj)
                session.add(embedding)
            session.add(obj)
            await session.commit()
        except IntegrityError:
            return print("in base")
        except Exception as e:
            print(e)
            raise print(e)
    return "imported"


async def main():
    csv_file_path = "/file/yappy_hackaton_2024_400k.csv"
    with open(csv_file_path, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            await add_video_task(row)
            time.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
