"""Add sicil_office_code and composite unique on (sicil_no, sicil_office_code)

Revision ID: d3f1a2b4c6e7
Revises: c5ad8926b2d5
Create Date: 2025-08-12 17:45:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd3f1a2b4c6e7'
down_revision = 'c5ad8926b2d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Yeni kolon
    op.add_column('companies', sa.Column('sicil_office_code', sa.String(length=64), nullable=True))
    # 2) Backfill: sicil_mudurluk'un ilk kelimesi, UPPER
    op.execute(
        """
        UPDATE companies
        SET sicil_office_code = UPPER(split_part(COALESCE(sicil_mudurluk, ''), ' ', 1))
        WHERE (sicil_office_code IS NULL OR sicil_office_code = '')
        """
    )
    # 3) Eski unique index'i kaldır (sicil_no)
    op.drop_index(op.f('ix_companies_sicil_no'), table_name='companies')
    # 4) sicil_no için non-unique index'i geri oluştur
    op.create_index(op.f('ix_companies_sicil_no'), 'companies', ['sicil_no'], unique=False)
    # 5) sicil_office_code için index
    op.create_index(op.f('ix_companies_sicil_office_code'), 'companies', ['sicil_office_code'], unique=False)
    # 6) Bileşik unique constraint
    op.create_unique_constraint('ux_companies_sicil_no_office', 'companies', ['sicil_no', 'sicil_office_code'])


def downgrade() -> None:
    # 1) Bileşik unique constraint'i kaldır
    op.drop_constraint('ux_companies_sicil_no_office', 'companies', type_='unique')
    # 2) sicil_office_code index'ini kaldır
    op.drop_index(op.f('ix_companies_sicil_office_code'), table_name='companies')
    # 3) sicil_no non-unique index'ini kaldır, unique geri oluştur
    op.drop_index(op.f('ix_companies_sicil_no'), table_name='companies')
    op.create_index(op.f('ix_companies_sicil_no'), 'companies', ['sicil_no'], unique=True)
    # 4) Kolonu kaldır
    op.drop_column('companies', 'sicil_office_code')
