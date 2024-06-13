import re
import aiohttp

from app.models import Tag


TAG_PATTERN = r'#\w+'


def parse_tags(description):
    tags = re.findall(TAG_PATTERN, description)
    return [tag.lower()[1:] for tag in tags]


async def check_and_add_tags(session, tag_list):
    existing_tags = await session.query(Tag).filter(
        Tag.name.in_(tag_list)
    ).all()
    existing_tag_names = {tag.name for tag in existing_tags}
    new_tags = [Tag(name=tag)
                for tag in tag_list if tag not in existing_tag_names]
    session.add_all(new_tags)
    await session.commit()
    existing_tags.extend(new_tags)
    return existing_tags


async def convert_text_to_embeddings(texts):
    async with aiohttp.ClientSession() as session:
        texts = [text.replace("\n", " ") for text in texts]
        response = await session.post(
            url='http://localhost:8082',
            json={
                "inputs": texts,
                "task": "feature-extraction",
                "parameters": {}
            },
        )
    return (await response.json())[0]


def remove_tags(description):
    cleaned_description = re.sub(TAG_PATTERN, '', description)
    return cleaned_description.strip()
