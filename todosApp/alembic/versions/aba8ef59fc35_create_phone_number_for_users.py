"""create phone number for users

Revision ID: aba8ef59fc35
Revises: 
Create Date: 2024-06-09 11:56:37.463722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aba8ef59fc35'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(10),nullable=True))


def downgrade() -> None:
    pass