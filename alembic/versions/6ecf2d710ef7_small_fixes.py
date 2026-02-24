"""small fixes

Revision ID: 6ecf2d710ef7
Revises: 341ebf18c0ef
Create Date: 2026-02-21 00:31:54.383744

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6ecf2d710ef7"
down_revision: Union[str, Sequence[str], None] = "341ebf18c0ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
