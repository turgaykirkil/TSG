"""Add UNIQUE(announcement_id, item_index) to ocr_results

Revision ID: b1c2d3e4f5a6
Revises: f0d1e2c3b4a5
Create Date: 2025-10-10 08:55:00.000000

Bu migration, Supabase uzerinde MCP ile uygulanan degisikligi (UNIQUE kisit) repoya belgelemek icindir.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text as sa_text

# revision identifiers, used by Alembic.
revision = 'b1c2d3e4f5a6'
down_revision = 'f0d1e2c3b4a5'
branch_labels = None
depends_on = None

CONSTRAINT_NAME = 'ocr_results_uq_announcement_item'
TABLE_NAME = 'ocr_results'
COLUMNS = ['announcement_id', 'item_index']

def _constraint_exists(conn) -> bool:
    q = sa_text("""
        SELECT 1
        FROM pg_constraint
        WHERE conname = :name
        LIMIT 1
    """)
    res = conn.execute(q, {"name": CONSTRAINT_NAME}).fetchone()
    return bool(res)


def upgrade() -> None:
    bind = op.get_bind()
    if not _constraint_exists(bind):
        try:
            op.create_unique_constraint(CONSTRAINT_NAME, TABLE_NAME, COLUMNS)
        except Exception:
            # Son care olarak raw SQL ile dene (idempotent olmayabilir)
            op.execute(
                sa_text(
                    f"ALTER TABLE public.{TABLE_NAME} ADD CONSTRAINT {CONSTRAINT_NAME} UNIQUE (announcement_id, item_index)"
                )
            )


def downgrade() -> None:
    try:
        op.drop_constraint(CONSTRAINT_NAME, TABLE_NAME, type_='unique')
    except Exception:
        # Varsa silinsin; yoksa sessiz gec
        pass
