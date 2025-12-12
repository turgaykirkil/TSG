import sys
import os
import asyncio
from sqlalchemy import text
from uuid import UUID

# Add backend to path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.nexus.graph_service import NexusGraphService
from app.api.api_v1.endpoints.processing import process_background_geocoding

async def verify_logic():
    db = SessionLocal()
    target_id = "c0041c75-0768-4279-8c1e-939bc61ecfbe"
    
    try:
        print(f"🧪 Starting Service-Level Geocoding Verification for {target_id}...")
        
        # 1. Sabotage
        print("💥 Sabotage: Deleting coordinates...")
        db.execute(text(f"UPDATE public.companies SET koordinat = NULL WHERE id = '{target_id}'"))
        db.commit()
        
        # 2. Service Analysis
        print("🧠 Running Nexus Graph Service...")
        service = NexusGraphService(db)
        # Limit 10 is enough
        result = service.analyze_company_network(UUID(target_id), limit=10)
        
        missing = result['analysis'].get('missing_coords', [])
        print(f"🕵️‍♂️ Service detected missing coords: {len(missing)} IDs.")
        
        if target_id in missing:
            print("✅ SUCCEES: Target ID correctly identified as missing coordinates.")
        else:
            print(f"❌ FAILURE: Target ID not detected. Missing: {missing}")
            return

        # 3. Simulate Background Task
        print("🔄 Simulating Background Task Processing...")
        await process_background_geocoding(missing)
        
        # 4. Verification
        print("🔍 Verification: Checking DB...")
        # New session/query to be sure
        data = db.execute(text(f"SELECT ST_AsText(koordinat) FROM public.companies WHERE id = '{target_id}'")).scalar()
        
        if data:
            print(f"🎉 SUCCESS! Coordinates restored: {data}")
        else:
            print("❌ FAILURE. Coordinates are still NULL.")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(verify_logic())
