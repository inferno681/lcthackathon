import re

import aiohttp

from app.core import config, TAG_PATTERN


def parse_tags(description: str) -> list[str]:
    """Функция парсинга тэгов из текста"""
    tags = re.findall(TAG_PATTERN, description)
    return [tag.lower()[1:] for tag in tags]


async def convert_text_to_embeddings(text: str) -> list[float]:
    """Функция получения эмбеддингов из текста"""
    async with aiohttp.ClientSession() as session:
        text = text.replace("\n", " ")
        response = await session.post(
            url=config.EMBEDDINGS_SERVER,
            json={
                "inputs": [text],
                "task": "feature-extraction",
                "parameters": {},
            },
        )
    return (await response.json())[0]


def remove_tags(description: str) -> str:
    """Функция удаления тэгов из текста"""
    cleaned_description = re.sub(TAG_PATTERN, "", description)
    return cleaned_description.strip()
