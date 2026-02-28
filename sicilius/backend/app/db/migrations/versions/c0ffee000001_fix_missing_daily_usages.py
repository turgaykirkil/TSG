"""fix missing daily_usages

Revision ID: c0ffee000001
Revises: bf1009336cbe
Create Date: 2026-01-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c0ffee000001'
down_revision = 'bf1009336cbe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if table exists to avoid error if it was manually created
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names(schema='app')
    if 'daily_usages' not in tables:
        op.create_table('daily_usages',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('user_id', sa.UUID(), nullable=False),
            sa.Column('day', sa.Date(), nullable=False),
            sa.Column('count', sa.Integer(), nullable=False, server_default=sa.text('0')),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id', 'day', name='uq_daily_usage_user_day'),
            schema='app'
        )
        op.create_index(op.f('ix_app_daily_usages_day'), 'daily_usages', ['day'], unique=False, schema='app')
        op.create_index(op.f('ix_app_daily_usages_user_id'), 'daily_usages', ['user_id'], unique=False, schema='app')


def downgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names(schema='app')
    if 'daily_usages' in tables:
        op.drop_table('daily_usages', schema='app')
