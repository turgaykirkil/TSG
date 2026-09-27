"""expand person columns

Revision ID: 7f5142928709
Revises: 5e3142928708
Create Date: 2026-08-30 21:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7f5142928709'
down_revision = '5e3142928708'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('persons', 'masked_id',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True,
               schema='app')
    op.alter_column('persons', 'nationality_id',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True,
               schema='app')
    op.alter_column('persons', 'phone',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True,
               schema='app')


def downgrade():
    op.alter_column('persons', 'phone',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True,
               schema='app')
    op.alter_column('persons', 'nationality_id',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True,
               schema='app')
    op.alter_column('persons', 'masked_id',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True,
               schema='app')
