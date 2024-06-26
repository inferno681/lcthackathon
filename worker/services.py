import re

from langchain_huggingface import HuggingFaceEndpointEmbeddings
from sqlalchemy import select

from config import config
from models import Tag

embeddings = HuggingFaceEndpointEmbeddings(model=config.EMBEDDINGS_URL)


def parse_tags(description: str) -> list:
    tags = re.findall(r"#\w+", description)
    return [tag.lower()[1:] for tag in tags]


async def check_and_add_tags(session, tag_list: list) -> list:
    result = await session.execute(select(Tag).filter(Tag.name.in_(tag_list)))
    existing_tags = result.scalars().all()
    existing_tag_names = {tag.name for tag in existing_tags}
    new_tags = [
        Tag(name=tag) for tag in tag_list if tag not in existing_tag_names
    ]
    session.add_all(new_tags)
    await session.commit()
    existing_tags.extend(new_tags)
    return existing_tags


async def convert_text_to_embeddings(text: str) -> list:
    return await embeddings.aembed_query(text)
