"""
Add scraped_at column to companies table
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('companies', sa.Column('scraped_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('companies', 'scraped_at')
