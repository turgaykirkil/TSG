"""Set ON DELETE SET NULL for ocr_results.announcement_id

Revision ID: f0d1e2c3b4a5
Revises: e7b2c3d4e5f6
Create Date: 2025-08-13 21:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f0d1e2c3b4a5'
down_revision = 'e7b2c3d4e5f6'
branch_labels = None
depends_on = None


def _find_announcement_fk_name(conn) -> str | None:
    insp = sa.inspect(conn)
    for fk in insp.get_foreign_keys('ocr_results'):
        cols = fk.get('constrained_columns') or []
        ref_table = fk.get('referred_table')
        if ref_table == 'announcements' and cols == ['announcement_id']:
            return fk.get('name')
    return None


def upgrade() -> None:
    bind = op.get_bind()

    # Ensure column is nullable
    op.alter_column('ocr_results', 'announcement_id', existing_type=sa.UUID(), nullable=True)

    # Drop existing FK (if any) and recreate with ON DELETE SET NULL
    fk_name = _find_announcement_fk_name(bind)
    if fk_name:
        try:
            op.drop_constraint(fk_name, 'ocr_results', type_='foreignkey')
        except Exception:
            pass
    op.create_foreign_key(
        'fk_ocr_results_announcement_id',
        'ocr_results',
        'announcements',
        ['announcement_id'],
        ['id'],
        ondelete='SET NULL',
    )


def downgrade() -> None:
    bind = op.get_bind()

    # Drop the ON DELETE SET NULL FK
    try:
        op.drop_constraint('fk_ocr_results_announcement_id', 'ocr_results', type_='foreignkey')
    except Exception:
        # Fallback: try to detect FK name dynamically
        fk_name = _find_announcement_fk_name(bind)
        if fk_name:
            op.drop_constraint(fk_name, 'ocr_results', type_='foreignkey')

    # Recreate FK without ON DELETE behavior
    op.create_foreign_key(
        'fk_ocr_results_announcement_id',
        'ocr_results',
        'announcements',
        ['announcement_id'],
        ['id'],
        ondelete=None,
    )
