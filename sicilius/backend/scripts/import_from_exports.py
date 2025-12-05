import os, sys, json
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, date

DSN = os.getenv("TSG_DATABASE_URL") or os.getenv("DATABASE_URL") or ""
EXPORTS_DIR = os.getenv("EXPORTS_DIR", os.path.join(os.path.dirname(__file__), "..", "exports"))

if not DSN:
    print("ERROR: TSG_DATABASE_URL/DATABASE_URL not set")
    sys.exit(1)

# Helpers

def read_ndjson(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue

def to_date(v):
    if not v:
        return None
    try:
        return date.fromisoformat(str(v))
    except Exception:
        return None

def to_ts(v):
    if not v:
        return None
    try:
        return datetime.fromisoformat(str(v))
    except Exception:
        return None

# Importers

def import_companies(cur):
    path = os.path.join(EXPORTS_DIR, "companies.ndjson")
    if not os.path.exists(path):
        print("companies.ndjson not found, skipping")
        return
    cols = [
        "id","unvan","mersis_number","phone","email","website","address",
        "district","city","country","is_active","establishment_date","scraped_at",
        "created_at","updated_at","sicil_mudurluk","sicil_no","sicil_office_code",
        "nace_code","pdf_name","pdf_path"
    ]
    rows = []
    total = 0
    for obj in read_ndjson(path):
        total += 1
        rows.append([
            obj.get("id"),
            obj.get("unvan"),
            obj.get("mersis_number"),
            obj.get("phone"),
            obj.get("email"),
            obj.get("website"),
            obj.get("address"),
            obj.get("district"),
            obj.get("city"),
            obj.get("country") or "Türkiye",
            bool(obj.get("is_active", True)),
            to_date(obj.get("establishment_date")),
            to_ts(obj.get("scraped_at")),
            to_ts(obj.get("created_at")),
            to_ts(obj.get("updated_at")),
            obj.get("sicil_mudurluk"),
            obj.get("sicil_no"),
            obj.get("sicil_office_code"),
            obj.get("nace_code"),
            obj.get("pdf_name"),
            obj.get("pdf_path"),
        ])
        if len(rows) >= 2000:
            execute_values(cur,
                f"""
                INSERT INTO companies ({','.join(cols)})
                VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                  unvan=EXCLUDED.unvan,
                  mersis_number=EXCLUDED.mersis_number,
                  phone=EXCLUDED.phone,
                  email=EXCLUDED.email,
                  website=EXCLUDED.website,
                  address=EXCLUDED.address,
                  district=EXCLUDED.district,
                  city=EXCLUDED.city,
                  country=EXCLUDED.country,
                  is_active=EXCLUDED.is_active,
                  establishment_date=EXCLUDED.establishment_date,
                  scraped_at=EXCLUDED.scraped_at,
                  created_at=EXCLUDED.created_at,
                  updated_at=EXCLUDED.updated_at,
                  sicil_mudurluk=EXCLUDED.sicil_mudurluk,
                  sicil_no=EXCLUDED.sicil_no,
                  sicil_office_code=EXCLUDED.sicil_office_code,
                  nace_code=EXCLUDED.nace_code,
                  pdf_name=EXCLUDED.pdf_name,
                  pdf_path=EXCLUDED.pdf_path
                """,
                rows,
                page_size=2000
            )
            rows.clear()
            print(f"companies: inserted/upserted ~{total}")
    if rows:
        execute_values(cur,
            f"""
            INSERT INTO companies ({','.join(cols)})
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
              unvan=EXCLUDED.unvan,
              mersis_number=EXCLUDED.mersis_number,
              phone=EXCLUDED.phone,
              email=EXCLUDED.email,
              website=EXCLUDED.website,
              address=EXCLUDED.address,
              district=EXCLUDED.district,
              city=EXCLUDED.city,
              country=EXCLUDED.country,
              is_active=EXCLUDED.is_active,
              establishment_date=EXCLUDED.establishment_date,
              scraped_at=EXCLUDED.scraped_at,
              created_at=EXCLUDED.created_at,
              updated_at=EXCLUDED.updated_at,
              sicil_mudurluk=EXCLUDED.sicil_mudurluk,
              sicil_no=EXCLUDED.sicil_no,
              sicil_office_code=EXCLUDED.sicil_office_code,
              nace_code=EXCLUDED.nace_code,
              pdf_name=EXCLUDED.pdf_name,
              pdf_path=EXCLUDED.pdf_path
            """,
            rows,
            page_size=2000
        )
        print(f"companies: inserted/upserted {total}")


def import_announcements(cur):
    path = os.path.join(EXPORTS_DIR, "announcements.ndjson")
    if not os.path.exists(path):
        print("announcements.ndjson not found, skipping")
        return
    cols = [
        "id","trade_registry_name","trade_registry_number","title","publication_date",
        "issue_number","page_number","announcement_type","newspaper_name","pdf_url",
        "company_id","created_at","updated_at"
    ]
    rows = []
    total = 0
    for obj in read_ndjson(path):
        total += 1
        rows.append([
            obj.get("id"),
            obj.get("trade_registry_name"),
            obj.get("trade_registry_number"),
            obj.get("title"),
            to_date(obj.get("publication_date")),
            obj.get("issue_number"),
            obj.get("page_number"),
            obj.get("announcement_type"),
            obj.get("newspaper_name"),
            obj.get("pdf_url"),
            obj.get("company_id"),
            to_ts(obj.get("created_at")),
            to_ts(obj.get("updated_at")),
        ])
        if len(rows) >= 5000:
            execute_values(cur,
                f"""
                INSERT INTO announcements ({','.join(cols)})
                VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                  trade_registry_name=EXCLUDED.trade_registry_name,
                  trade_registry_number=EXCLUDED.trade_registry_number,
                  title=EXCLUDED.title,
                  publication_date=EXCLUDED.publication_date,
                  issue_number=EXCLUDED.issue_number,
                  page_number=EXCLUDED.page_number,
                  announcement_type=EXCLUDED.announcement_type,
                  newspaper_name=EXCLUDED.newspaper_name,
                  pdf_url=EXCLUDED.pdf_url,
                  company_id=EXCLUDED.company_id,
                  created_at=EXCLUDED.created_at,
                  updated_at=EXCLUDED.updated_at
                """,
                rows,
                page_size=5000
            )
            rows.clear()
            print(f"announcements: upserted ~{total}")
    if rows:
        execute_values(cur,
            f"""
            INSERT INTO announcements ({','.join(cols)})
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
              trade_registry_name=EXCLUDED.trade_registry_name,
              trade_registry_number=EXCLUDED.trade_registry_number,
              title=EXCLUDED.title,
              publication_date=EXCLUDED.publication_date,
              issue_number=EXCLUDED.issue_number,
              page_number=EXCLUDED.page_number,
              announcement_type=EXCLUDED.announcement_type,
              newspaper_name=EXCLUDED.newspaper_name,
              pdf_url=EXCLUDED.pdf_url,
              company_id=EXCLUDED.company_id,
              created_at=EXCLUDED.created_at,
              updated_at=EXCLUDED.updated_at
            """,
            rows,
            page_size=5000
        )
        print(f"announcements: upserted {total}")


def import_ocr_results(cur):
    path = os.path.join(EXPORTS_DIR, "ocr_results.ndjson")
    if not os.path.exists(path):
        print("ocr_results.ndjson not found, skipping")
        return
    cols = [
        "id","announcement_id","company_id","raw_text","structured_data","status",
        "created_at","updated_at"
    ]
    rows = []
    total = 0
    for obj in read_ndjson(path):
        total += 1
        rows.append([
            obj.get("id"),
            obj.get("announcement_id"),
            obj.get("company_id"),
            obj.get("original_text"),
            obj.get("structured_data"),
            obj.get("status") or "pending",
            to_ts(obj.get("created_at")),
            to_ts(obj.get("updated_at")),
        ])
        if len(rows) >= 2000:
            execute_values(cur,
                f"""
                INSERT INTO ocr_results ({','.join(cols)})
                VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                  announcement_id=EXCLUDED.announcement_id,
                  company_id=EXCLUDED.company_id,
                  raw_text=EXCLUDED.raw_text,
                  structured_data=EXCLUDED.structured_data,
                  status=EXCLUDED.status,
                  created_at=EXCLUDED.created_at,
                  updated_at=EXCLUDED.updated_at
                """,
                rows,
                page_size=2000
            )
            rows.clear()
            print(f"ocr_results: upserted ~{total}")
    if rows:
        execute_values(cur,
            f"""
            INSERT INTO ocr_results ({','.join(cols)})
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
              announcement_id=EXCLUDED.announcement_id,
              company_id=EXCLUDED.company_id,
              raw_text=EXCLUDED.raw_text,
              structured_data=EXCLUDED.structured_data,
              status=EXCLUDED.status,
              created_at=EXCLUDED.created_at,
              updated_at=EXCLUDED.updated_at
            """,
            rows,
            page_size=2000
        )
        print(f"ocr_results: upserted {total}")


def main():
    target = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as cur:
            # Ensure we target the public schema
            try:
                cur.execute("SET search_path TO public")
            except Exception:
                pass
            if target in ("all", "companies"):
                print("Importing companies...")
                import_companies(cur)
            if target in ("all", "announcements"):
                print("Importing announcements...")
                import_announcements(cur)
            if target in ("all", "ocr"):
                print("Importing ocr_results...")
                import_ocr_results(cur)
    print("Done.")

if __name__ == "__main__":
    main()
