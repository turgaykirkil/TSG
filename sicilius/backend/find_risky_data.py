import sys
import os

# Add backend directory to path so we can import app modules
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.company import Company
from sqlalchemy import func, desc, or_

def find_risky_data():
    db = SessionLocal()
    try:
        print("\n--- 1. İFLAS / KONKORDATO / TASFİYE İçeren Şirketler ---")
        keywords = ["İFLAS", "KONKORDATO", "TASFİYE"]
        found = False
        for kw in keywords:
            comps = db.query(Company).filter(Company.unvan.ilike(f"%{kw}%")).limit(3).all()
            for c in comps:
                found = True
                print(f"🔴 [{kw}] {c.unvan}")
                print(f"   ID: {c.id}")
        
        if not found:
            print("❌ Bu kriterde şirket bulunamadı.")

        print("\n--- 2. Adres Kümelenmesi (Aynı Adreste >3 Şirket) ---")
        # Simple exact match grouping
        dupes = db.query(Company.address, func.count(Company.id))\
            .filter(Company.address.isnot(None))\
            .group_by(Company.address)\
            .having(func.count(Company.id) > 3)\
            .order_by(desc(func.count(Company.id)))\
            .limit(5).all()
        
        if not dupes:
             print("❌ Yoğun adres kümelenmesi bulunamadı.")
        else:
            for addr, count in dupes:
                print(f"🟠 [ADRES] {count} Şirket | {addr[:60]}...")
                # Get example companies at this address
                examples = db.query(Company).filter(Company.address == addr).limit(3).all()
                for ex in examples:
                    print(f"   -> {ex.unvan}")

    finally:
        db.close()

if __name__ == "__main__":
    find_risky_data()
