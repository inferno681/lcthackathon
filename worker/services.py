import re
import aiohttp
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from .config import config
from app.models import Tag

embeddings = HuggingFaceEndpointEmbeddings(model=config.EMBEDDINGS_SERVER)


def parse_tags(description):
    tags = re.findall(r'#\w+', description)
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


async def convert_text_to_embeddings(text):
    return embeddings.embed_query(text)


async def send_file_to_fastapi(file_path, url):
    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file, filename=file_path)
            async with session.post(url, data=form_data) as response:
                if response.status == 200:
                    print("Файл успешно отправлен!")
                else:
                    print(f"Ошибка {response.status} при отправке файла.")
