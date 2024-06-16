from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    Table,
    Text,
    Integer,
    TIMESTAMP,
    Sequence,
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from db import Base


yappi_tag = Table(
    "yappi_tag",
    Base.metadata,
    Column(
        "yappi_id",
        BigInteger,
        ForeignKey("public.yappi.id", ondelete="CASCADE"),
    ),
    Column(
        "tag_id", BigInteger, ForeignKey("public.tag.id", ondelete="CASCADE")
    ),
)


class Yappi(Base):
    """Таблица с информацией о загруженных видео"""

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
    create_time = Column(TIMESTAMP, default=datetime.now)
    popularity = Column(Integer)
    embeddings = relationship("Embedding", back_populates="yappi")
    tags = relationship("Tag", secondary=yappi_tag, back_populates="yappis")


class Tag(Base):
    """Таблица с тэгами"""

    __tablename__ = "tag"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("tag_id_seq", schema="public")
    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    name = Column(String, nullable=False, unique=True)

    yappis = relationship("Yappi", secondary=yappi_tag, back_populates="tags")


class Embedding(Base):
    """Таблица векторов"""

    __tablename__ = "embedding"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("embedding_id_seq", schema="public")
    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    yappi_id = Column(
        BigInteger, ForeignKey("public.yappi.id", ondelete="CASCADE")
    )
    embedding = Column(Vector(384))
    yappi = relationship("Yappi", back_populates="embeddings")
