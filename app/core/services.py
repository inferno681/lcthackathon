import re

from app.models import Tag


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
