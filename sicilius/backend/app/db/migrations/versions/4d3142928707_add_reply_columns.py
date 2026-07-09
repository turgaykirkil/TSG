"""add reply columns

Revision ID: 4d3142928707
Revises: c627952a2863
Create Date: 2026-07-08 22:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4d3142928707'
down_revision = 'c627952a2863'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to app.contact_messages
    op.add_column('contact_messages', sa.Column('reply_text', sa.Text(), nullable=True), schema='app')
    op.add_column('contact_messages', sa.Column('replied_at', sa.DateTime(), nullable=True), schema='app')
    
    # Add columns to app.incoming_emails
    op.add_column('incoming_emails', sa.Column('reply_text', sa.Text(), nullable=True), schema='app')
    op.add_column('incoming_emails', sa.Column('replied_at', sa.DateTime(timezone=True), nullable=True), schema='app')


def downgrade() -> None:
    op.drop_column('incoming_emails', 'replied_at', schema='app')
    op.drop_column('incoming_emails', 'reply_text', schema='app')
    op.drop_column('contact_messages', 'replied_at', schema='app')
    op.drop_column('contact_messages', 'reply_text', schema='app')
