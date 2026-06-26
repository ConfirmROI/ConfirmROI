"""add cost tracking tables and columns

Revision ID: b3c4d5e6f7a8
Revises: a1b2c3d4e5f6
Create Date: 2026-06-24 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c4d5e6f7a8'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cost_entries',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category', sa.Enum('development', 'infrastructure', 'vendor', 'other', name='costcategory'), nullable=False, server_default='development'),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('person_weeks', sa.Numeric(10, 2), nullable=True),
        sa.Column('amount', sa.Numeric(20, 4), nullable=False, server_default='0'),
        sa.Column('cost_type', sa.Enum('one_time', 'recurring_monthly', 'recurring_annual', name='costtype'), nullable=False, server_default='one_time'),
        sa.Column('incurred_date', sa.Date(), nullable=True),
        sa.Column('is_estimate', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.add_column('teams', sa.Column('avg_labor_cost_per_week', sa.Numeric(10, 2), nullable=True))
    op.add_column('users', sa.Column('default_labor_cost_per_week', sa.Numeric(10, 2), nullable=True))


def downgrade():
    op.drop_column('users', 'default_labor_cost_per_week')
    op.drop_column('teams', 'avg_labor_cost_per_week')
    op.drop_table('cost_entries')
    sa.Enum(name='costtype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='costcategory').drop(op.get_bind(), checkfirst=True)
