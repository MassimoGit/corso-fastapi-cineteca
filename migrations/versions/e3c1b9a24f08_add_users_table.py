"""add users table

Revision ID: e3c1b9a24f08
Revises: 7b2d4e91c3a5
Create Date: 2026-11-14 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e3c1b9a24f08'
down_revision: Union[str, Sequence[str], None] = '7b2d4e91c3a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aggiunge la tabella users nello schema cineteca."""
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), server_default='staff', nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('username'),
        schema='cineteca',
    )


def downgrade() -> None:
    """Rimuove la tabella users dallo schema cineteca."""
    op.drop_table('users', schema='cineteca')
