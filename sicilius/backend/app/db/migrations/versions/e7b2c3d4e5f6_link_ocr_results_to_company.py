"""Link OCR results to company and make announcement_id nullable

Revision ID: e7b2c3d4e5f6
Revises: d3f1a2b4c6e7
Create Date: 2025-08-13 17:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'e7b2c3d4e5f6'
down_revision = 'd3f1a2b4c6e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # 1) announcement_id'yi nullable yap (legacy alan)
    ocr_cols = {c['name']: c for c in insp.get_columns('ocr_results')}
    if 'announcement_id' in ocr_cols:
        if not ocr_cols['announcement_id'].get('nullable', True):
            op.alter_column('ocr_results', 'announcement_id', existing_type=sa.UUID(), nullable=True)

    # 2) company_id kolonu ekle (önce nullable)
    if 'company_id' not in ocr_cols:
        op.add_column('ocr_results', sa.Column('company_id', sa.UUID(), nullable=True))

    # Inspector'ı tazele
    ocr_cols = {c['name']: c for c in insp.get_columns('ocr_results')}

    # 3) FK ve index ekle (geçici olarak nullable)
    existing_indexes = {idx['name'] for idx in insp.get_indexes('ocr_results')}
    if op.f('ix_ocr_results_company_id') not in existing_indexes:
        op.create_index(op.f('ix_ocr_results_company_id'), 'ocr_results', ['company_id'], unique=False)

    existing_fks = insp.get_foreign_keys('ocr_results')
    has_fk = any(
        fk.get('referred_table') == 'companies' and fk.get('constrained_columns') == ['company_id']
        for fk in existing_fks
    )
    if not has_fk:
        op.create_foreign_key('fk_ocr_results_company_id', 'ocr_results', 'companies', ['company_id'], ['id'])

    # 4) Backfill: announcement -> company aktarımı (yalnızca company_id NULL ise anlamlı)
    op.execute(
        """
        UPDATE ocr_results AS o
        SET company_id = a.company_id
        FROM announcements AS a
        WHERE o.announcement_id = a.id AND o.company_id IS NULL
        """
    )

    # 5) company_id zorunlu yap (NULL var mı kontrol et)
    null_count = bind.execute(sa.text("SELECT COUNT(*) FROM ocr_results WHERE company_id IS NULL")).scalar()
    if null_count == 0:
        op.alter_column('ocr_results', 'company_id', nullable=False, existing_type=sa.UUID())


def downgrade() -> None:
    # 1) company_id tekrar nullable yapıp FK ve index'i kaldır
    try:
        op.alter_column('ocr_results', 'company_id', nullable=True, existing_type=sa.UUID())
    except Exception:
        pass
    try:
        op.drop_constraint('fk_ocr_results_company_id', 'ocr_results', type_='foreignkey')
    except Exception:
        pass
    try:
        op.drop_index(op.f('ix_ocr_results_company_id'), table_name='ocr_results')
    except Exception:
        pass

    # 2) Kolonu kaldır
    op.drop_column('ocr_results', 'company_id')

    # 3) announcement_id'yi tekrar NOT NULL yap (eski duruma dönüş)
    try:
        op.alter_column('ocr_results', 'announcement_id',
                        existing_type=sa.UUID(),
                        nullable=False)
    except Exception:
        pass
