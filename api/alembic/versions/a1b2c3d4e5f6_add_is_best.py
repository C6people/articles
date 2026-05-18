"""add is_best to question_comments

Revision ID: a1b2c3d4e5f6
Revises: 9f528050ceeb
Create Date: 2026-05-18 10:57:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '9f528050ceeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('question_comments', sa.Column('is_best', sa.Boolean(), nullable=False, server_default=sa.text('false'), comment='ベストアンサー'))


def downgrade() -> None:
    op.drop_column('question_comments', 'is_best')
