"""init_migration

Revision ID: 508b80674b4c
Revises:
Create Date: 2024-06-15 10:19:59.272156

"""

from typing import Sequence, Union

import pgvector
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "508b80674b4c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE EXTENSION IF NOT EXISTS vector;
    """
    )
    op.execute(
        """
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
    """
    )
    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS public.yappi_id_seq;
    """
    )
    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS public.tag_id_seq;
    """
    )
    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS public.yappi_tag_id_seq;
    """
    )
    op.execute(
        """
        CREATE SEQUENCE IF NOT EXISTS public.vector_id_seq;
    """
    )
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vector",
        sa.Column(
            "id",
            sa.BigInteger(),
            server_default=sa.text("nextval('public.vector_id_seq')"),
            nullable=False,
        ),
        sa.Column(
            "vector", pgvector.sqlalchemy.Vector(dim=384), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_table(
        "tag",
        sa.Column(
            "id",
            sa.BigInteger(),
            server_default=sa.text("nextval('public.tag_id_seq')"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="public",
    )
    op.create_table(
        "yappi",
        sa.Column(
            "id",
            sa.BigInteger(),
            server_default=sa.text("nextval('public.yappi_id_seq')"),
            nullable=False,
        ),
        sa.Column("link", sa.String(), nullable=False),
        sa.Column("face", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("voise_description", sa.String(), nullable=True),
        sa.Column("image_description", sa.String(), nullable=True),
        sa.Column("full_description", sa.Text(), nullable=True),
        sa.Column("create_time", sa.TIMESTAMP(), nullable=True),
        sa.Column("popularity", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("face"),
        sa.UniqueConstraint("link"),
        schema="public",
    )
    op.create_table(
        "yappi_tag",
        sa.Column(
            "id",
            sa.BigInteger(),
            server_default=sa.text("nextval('public.yappi_tag_id_seq')"),
            nullable=False,
        ),
        sa.Column("yappi_id", sa.BigInteger(), nullable=True),
        sa.Column("tag_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["public.tag.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["yappi_id"], ["public.yappi.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    # ### end Alembic commands ###
    op.execute(
        """
        CREATE INDEX trgm_full_description_idx ON yappi USING gist (full_description gist_trgm_ops);
    """  # noqa
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("yappi_tag", schema="public")
    op.drop_table("yappi", schema="public")
    op.drop_table("tag", schema="public")
    op.drop_table("Vector", schema="public")
    # ### end Alembic commands ###
