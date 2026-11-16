"""add rooms is_accessible

Revision ID: 9d3e7b61a420
Revises: 4a8c1f29e03b
Create Date: 2026-11-14 09:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d3e7b61a420'
down_revision: Union[str, Sequence[str], None] = '4a8c1f29e03b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'rooms',
        sa.Column('is_accessible', sa.Boolean(), server_default=sa.false(), nullable=False),
        schema='cineteca',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('rooms', 'is_accessible', schema='cineteca')
