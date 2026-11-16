"""add spectators table

Revision ID: 7b2d4e91c3a5
Revises: f16b82c40d59
Create Date: 2026-11-14 14:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b2d4e91c3a5'
down_revision: Union[str, Sequence[str], None] = 'f16b82c40d59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aggiunge la tabella spectators nello schema cineteca."""
    op.create_table(
        'spectators',
        sa.Column('spectator_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.Column('token', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('spectator_id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('token'),
        schema='cineteca',
    )


def downgrade() -> None:
    """Rimuove la tabella spectators dallo schema cineteca."""
    op.drop_table('spectators', schema='cineteca')
