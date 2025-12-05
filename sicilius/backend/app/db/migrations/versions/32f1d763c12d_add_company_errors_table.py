"""Add company_errors table

Revision ID: 32f1d763c12d
Revises: ed6e2c491f42
Create Date: 2025-12-05 21:45:56.879653

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '32f1d763c12d'
down_revision = 'ed6e2c491f42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('company_errors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['app.companies.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['app.app_users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='app'
    )
    op.create_index(op.f('ix_app_company_errors_id'), 'company_errors', ['id'], unique=False, schema='app')


def downgrade() -> None:
    op.drop_index(op.f('ix_app_company_errors_id'), table_name='company_errors', schema='app')
    op.drop_table('company_errors', schema='app')
