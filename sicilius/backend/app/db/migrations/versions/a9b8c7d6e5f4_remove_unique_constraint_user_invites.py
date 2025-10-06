"""Remove unique constraint uq_invite_inviter_month on user_invites

Revision ID: a9b8c7d6e5f4
Revises: efc3f55cc8c7
Create Date: 2025-10-05 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a9b8c7d6e5f4'
down_revision = 'efc3f55cc8c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    try:
        existing = [uc.get('name') for uc in insp.get_unique_constraints('user_invites')]
    except Exception:
        existing = []
    if 'uq_invite_inviter_month' in existing:
        try:
            op.drop_constraint('uq_invite_inviter_month', 'user_invites', type_='unique')
        except Exception:
            # In case of platform differences or if already dropped
            pass


def downgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    try:
        existing = [uc.get('name') for uc in insp.get_unique_constraints('user_invites')]
    except Exception:
        existing = []
    if 'uq_invite_inviter_month' not in existing:
        try:
            op.create_unique_constraint(
                'uq_invite_inviter_month',
                'user_invites',
                ['inviter_user_id', 'invited_month_key']
            )
        except Exception:
            # If creation fails due to duplicates, leave as-is on downgrade
            pass
