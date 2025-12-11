import sys
import os
from sqlalchemy import func, desc

# Add backend directory to path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.company import Company
from app.models.relation import CompanyPersonRelation

def find_connected_companies():
    db = SessionLocal()
    try:
        print("\n--- İlişkisi En Çok Olan Şirketler (Graph için İdeal) ---")
        # Count relations per company
        # relation.company_id is the source
        top_companies = db.query(
            CompanyPersonRelation.company_id,
            func.count().label('rel_count')
        ).group_by(CompanyPersonRelation.company_id)\
         .order_by(desc('rel_count'))\
         .limit(5).all()

        if not top_companies:
            print("❌ Hiç ilişki kaydı bulunamadı (CompanyPersonRelation tablosu boş olabilir).")
        else:
            for cid, count in top_companies:
                comp = db.query(Company).filter(Company.id == cid).first()
                if comp:
                    print(f"🔗 [{count} İlişki] {comp.unvan}")
                    print(f"   ID: {comp.id}")

    finally:
        db.close()

if __name__ == "__main__":
    find_connected_companies()
