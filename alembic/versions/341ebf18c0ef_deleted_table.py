"""deleted table

Revision ID: 341ebf18c0ef
Revises: 60bbaf9ae476
Create Date: 2026-02-21 00:12:58.312652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '341ebf18c0ef'
down_revision: Union[str, Sequence[str], None] = '60bbaf9ae476'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
