import os
import sys
import json
import uuid
from datetime import datetime, date

# Add project root to sys.path so we can import app modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.db.session import SessionLocal
from app.models.company import Company
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult

def parse_uuid(val):
    if not val:
        return None
    try:
        return uuid.UUID(val)
    except Exception:
        return None

def parse_datetime(val):
    if not val:
        return None
    try:
        return datetime.fromisoformat(val.replace('Z', '+00:00'))
    except Exception:
        return None

def parse_date(val):
    if not val:
        return None
    try:
        return date.fromisoformat(val)
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python scripts/restore_from_jsonl.py <backup_dir>")
        sys.exit(1)
        
    backup_dir = sys.argv[1]
    if not os.path.isdir(backup_dir):
        print(f"❌ Backup directory not found: {backup_dir}")
        sys.exit(1)

    db = SessionLocal()
    try:
        # Clear existing data first to allow running the script multiple times
        print("🗑️ Clearing existing data...")
        db.execute("TRUNCATE TABLE app.ocr_results, app.announcements, app.companies CASCADE;")
        db.commit()

        # 1. Restore Companies
        companies_file = os.path.join(backup_dir, "companies.jsonl")
        if os.path.exists(companies_file):
            print("🏢 Restoring companies...")
            companies_to_insert = []
            count = 0
            with open(companies_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    # Convert fields
                    item['id'] = parse_uuid(item.get('id'))
                    item['created_at'] = parse_datetime(item.get('created_at'))
                    item['updated_at'] = parse_datetime(item.get('updated_at'))
                    item['scraped_at'] = parse_datetime(item.get('scraped_at'))
                    item['establishment_date'] = parse_date(item.get('establishment_date'))
                    item.pop('unvan_unaccent', None)
                    
                    companies_to_insert.append(item)
                    count += 1
                    
                    if len(companies_to_insert) >= 1000:
                        db.bulk_insert_mappings(Company, companies_to_insert)
                        db.commit()
                        print(f"  Inserted {count} companies...")
                        companies_to_insert = []
            
            if companies_to_insert:
                db.bulk_insert_mappings(Company, companies_to_insert)
                db.commit()
                print(f"  Inserted final {count} companies.")
        else:
            print("⚠️ companies.jsonl not found, skipping.")

        # Fetch valid company IDs
        print("🔍 Loading valid company IDs for validation...")
        valid_company_ids = set(r[0] for r in db.query(Company.id).all())

        # 2. Restore Announcements
        announcements_file = os.path.join(backup_dir, "announcements.jsonl")
        if os.path.exists(announcements_file):
            print("📢 Restoring announcements...")
            announcements_to_insert = []
            count = 0
            skipped_count = 0
            with open(announcements_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    # Convert fields
                    item['id'] = parse_uuid(item.get('id'))
                    
                    company_id = parse_uuid(item.get('company_id'))
                    if company_id not in valid_company_ids:
                        skipped_count += 1
                        continue
                    
                    item['company_id'] = company_id
                    item['publication_date'] = parse_date(item.get('publication_date'))
                    item['created_at'] = parse_datetime(item.get('created_at'))
                    item['updated_at'] = parse_datetime(item.get('updated_at'))
                    
                    announcements_to_insert.append(item)
                    count += 1
                    
                    if len(announcements_to_insert) >= 2000:
                        db.bulk_insert_mappings(Announcement, announcements_to_insert)
                        db.commit()
                        print(f"  Inserted {count} announcements...")
                        announcements_to_insert = []
            
            if announcements_to_insert:
                db.bulk_insert_mappings(Announcement, announcements_to_insert)
                db.commit()
                print(f"  Inserted final {count} announcements. Skipped {skipped_count} orphans.")
            else:
                print(f"  Announcements restore complete. Inserted: {count}, Skipped: {skipped_count}")
        else:
            print("⚠️ announcements.jsonl not found, skipping.")

        # Fetch valid announcement IDs
        print("🔍 Loading valid announcement IDs for validation...")
        valid_announcement_ids = set(r[0] for r in db.query(Announcement.id).all())

        # 3. Restore OCR Results
        ocr_file = os.path.join(backup_dir, "ocr_results.jsonl")
        if os.path.exists(ocr_file):
            print("📄 Restoring ocr_results...")
            ocr_to_insert = []
            count = 0
            skipped_ocr_count = 0
            with open(ocr_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    
                    company_id = parse_uuid(item.get('company_id'))
                    announcement_id = parse_uuid(item.get('announcement_id'))
                    if company_id not in valid_company_ids or announcement_id not in valid_announcement_ids:
                        skipped_ocr_count += 1
                        continue
                        
                    item['company_id'] = company_id
                    item['announcement_id'] = announcement_id
                    item['publication_date'] = parse_datetime(item.get('publication_date'))
                    item['created_at'] = parse_datetime(item.get('created_at'))
                    item['updated_at'] = parse_datetime(item.get('updated_at'))
                    
                    ocr_to_insert.append(item)
                    count += 1
                    
                    if len(ocr_to_insert) >= 2000:
                        db.bulk_insert_mappings(OcrResult, ocr_to_insert)
                        db.commit()
                        print(f"  Inserted {count} ocr_results...")
                        ocr_to_insert = []
            
            if ocr_to_insert:
                db.bulk_insert_mappings(OcrResult, ocr_to_insert)
                db.commit()
                print(f"  Inserted final {count} ocr_results. Skipped {skipped_ocr_count} orphans.")
            else:
                print(f"  OCR results restore complete. Inserted: {count}, Skipped: {skipped_ocr_count}")
                
            # Update the serial sequence for ocr_results.id
            db.execute("SELECT setval(pg_get_serial_sequence('ocr_results', 'id'), coalesce(max(id), 1)) FROM ocr_results")
            db.commit()
            print("  Updated serial sequence for ocr_results.")
        else:
            print("⚠️ ocr_results.jsonl not found, skipping.")

        print("🎉 Database restore successfully completed!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during restore: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
