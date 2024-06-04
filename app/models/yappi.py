from datetime import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Integer,
    TIMESTAMP,
    Sequence
)
from pgvector.sqlalchemy import Vector

from app.core import Base


class Yappi(Base):
    __tablename__ = 'yappi'
    __table_args__ = {'schema': 'public'}

    id_seq = Sequence('yappi_id_seq', schema='public')

    id = Column(BigInteger, primary_key=True,
                server_default=id_seq.next_value())
    link = Column(String, nullable=False, unique=True)
    deskr_tags = Column(String,)
    deskr_voise = Column(String,)
    desk_image = Column(String,)
    deck_full = Column(Text,)
    desk_embedding = Column(Vector(1024))
    create_time = Column(TIMESTAMP, default=datetime.now)
    pop = Column(Integer)
