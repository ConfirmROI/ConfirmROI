"""add roi_value_3yr column

Revision ID: a1b2c3d4e5f6
Revises: 0244bf74bb08
Create Date: 2026-06-23 18:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '0244bf74bb08'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('roi_calculations', sa.Column('roi_value_3yr', sa.Numeric(20, 4), nullable=True))


def downgrade():
    op.drop_column('roi_calculations', 'roi_value_3yr')
