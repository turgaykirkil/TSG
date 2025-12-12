import asyncio
import sys
import os
import httpx

# Add backend to path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.api.api_v1.endpoints.processing import geocode_company_by_id
from app.models.company import Company

async def force_geocode():
    db = SessionLocal()
    try:
        # Find Nesil Ebatlama
        print("🔍 Searching for company...")
        company = db.query(Company).filter(Company.unvan.ilike('%NESİL EBATLAMA%')).first()
        
        if not company:
            print("❌ Company not found!")
            return

        print(f"✅ Found: {company.unvan}")
        print(f"🆔 ID: {company.id}")
        print(f"📍 Address: {company.address}")
        
        # Force Geocode
        print("🚀 Force Geocoding...")
        success = await geocode_company_by_id(db, company.id, company.address)
        
        if success:
            print("🎉 Success! Geocoding completed.")
            # Verify persistence
            db.refresh(company)
            print(f"🌍 New Coordinate: {company.koordinat}")
        else:
            print("❌ Geocoding Failed.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(force_geocode())
