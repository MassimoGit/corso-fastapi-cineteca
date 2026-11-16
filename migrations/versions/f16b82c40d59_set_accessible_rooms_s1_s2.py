"""set accessible rooms s1 s2

Revision ID: f16b82c40d59
Revises: 9d3e7b61a420
Create Date: 2026-11-14 09:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f16b82c40d59'
down_revision: Union[str, Sequence[str], None] = '9d3e7b61a420'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Le sale S1 (Sala Fellini) e S2 (Sala Leone) al piano terra sono accessibili.
    op.execute("UPDATE cineteca.rooms SET is_accessible = true WHERE code IN ('S1', 'S2')")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE cineteca.rooms SET is_accessible = false WHERE code IN ('S1', 'S2')")
