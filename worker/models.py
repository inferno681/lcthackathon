from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    String,
    Text,
    Integer,
    TIMESTAMP,
    Sequence,
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from db import Base


class YappiTag(Base):
    """Промежуточная таблица для М2М связи"""
    __tablename__ = "yappi_tag"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("yappi_tag_id_seq", schema="public")

    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    yappi_id = Column(BigInteger, ForeignKey(
        "public.yappi.id", ondelete="CASCADE"))
    tag_id = Column(BigInteger, ForeignKey(
        "public.tag.id", ondelete="CASCADE"))


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
    description = Column(String)
    voise_description = Column(String)
    image_description = Column(String)
    full_description = Column(Text)
    embedding_description = Column(Vector(384))
    create_time = Column(TIMESTAMP, default=datetime.now)
    popularity = Column(Integer)
    vectors = relationship("Vector", back_populates="yappis")
    tags = relationship(
        "Tag", secondary=YappiTag, back_populates="yappis"
    )


class Tag(Base):
    """Таблица с тэгами"""
    __tablename__ = "tag"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("tag_id_seq", schema="public")
    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    name = Column(String, nullable=False, unique=True)

    yappis = relationship(
        "Yappi", secondary=YappiTag, back_populates="tags"
    )


class Vectors(Base):
    """Таблица векторов"""
    __tablename__ = "Vector"
    __table_args__ = {"schema": "public"}

    id_seq = Sequence("vector_id_seq", schema="public")
    id = Column(
        BigInteger, primary_key=True, server_default=id_seq.next_value()
    )
    vector = Column(Vector(384))
    yappi = relationship("Yappi", back_populates="vectors")
