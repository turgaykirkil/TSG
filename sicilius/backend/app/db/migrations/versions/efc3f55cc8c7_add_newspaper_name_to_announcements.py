"""add newspaper_name to announcements

Revision ID: efc3f55cc8c7
Revises: f0d1e2c3b4a5
Create Date: 2025-08-13 22:56:33.655662

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'efc3f55cc8c7'
down_revision = 'f0d1e2c3b4a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Only ensure 'newspaper_name' exists on 'announcements'
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c['name'] for c in insp.get_columns('announcements')]
    if 'newspaper_name' not in cols:
        op.add_column('announcements', sa.Column('newspaper_name', sa.String(length=255), nullable=True))


def downgrade() -> None:
    # Drop 'newspaper_name' only if present
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c['name'] for c in insp.get_columns('announcements')]
    if 'newspaper_name' in cols:
        op.drop_column('announcements', 'newspaper_name')
