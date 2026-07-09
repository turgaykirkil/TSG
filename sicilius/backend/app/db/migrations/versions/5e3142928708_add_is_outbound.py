"""add is_outbound to incoming_emails

Revision ID: 5e3142928708
Revises: 4d3142928707
Create Date: 2026-07-08 22:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5e3142928708'
down_revision = '4d3142928707'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to app.incoming_emails
    op.add_column('incoming_emails', sa.Column('is_outbound', sa.Boolean(), server_default='false', nullable=False), schema='app')


def downgrade() -> None:
    op.drop_column('incoming_emails', 'is_outbound', schema='app')
