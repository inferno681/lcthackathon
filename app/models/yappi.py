from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    Text,
    Integer,
    Table,
    TIMESTAMP,
    Sequence,
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core import Base


yappi_tag_association = Table(
    "yappi_tag",
    Base.metadata,
    Column("yappi_id", BigInteger, ForeignKey("public.yappi.id")),
    Column("tag_id", BigInteger, ForeignKey("public.tag.id")),
)


class YappiTag(Base):
    __tablename__ = "yappi_tag"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("yappi_tag_id_seq", schema="public")

    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    yappi_id = Column(BigInteger, ForeignKey("public.yappi.id"))
    tag_id = Column(BigInteger, ForeignKey("public.tag.id"))


class Yappi(Base):
    __tablename__ = "yappi"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("yappi_id_seq", schema="public")

    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    link = Column(String, nullable=False, unique=True)
    face = Column(String, unique=True)
    tags_description = Column(String)
    voise_description = Column(String)
    image_description = Column(String)
    full_description = Column(Text)
    embedding_description = Column(Vector(384))
    create_time = Column(TIMESTAMP, default=datetime.now)
    popularity = Column(Integer)

    tags = relationship(
        "Tag", secondary=yappi_tag_association, back_populates="yappis"
    )


class Tag(Base):
    __tablename__ = "tag"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("tag_id_seq", schema="public")
    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    name = Column(String, nullable=False, unique=True)

    yappis = relationship(
        "Yappi", secondary=yappi_tag_association, back_populates="tags"
    )
