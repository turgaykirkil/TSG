#!/usr/bin/env python3
import re
import sys
from typing import Optional, Tuple
from datetime import date

from sqlalchemy import text

# Reuse app context
from app.core.supabase_client import supabase
from app.db.session import SessionLocal

CUTOFF_DATE = date(2021, 1, 1)
MARKER_VALUE = "pre-2021"

PUBLIC_PREFIX = "/storage/v1/object/public/"
SIGN_PREFIX = "/storage/v1/object/sign/"


def parse_bucket_and_path(pdf_url: str) -> Optional[Tuple[str, str]]:
    """
    Extract bucket and object path from a Supabase Storage URL.
    Supports both public and signed URL formats.
    Returns (bucket, object_path) or None if not parsable.
    """
    try:
        # Strip domain, focus on path after '/storage/v1/object/(public|sign)/'
        if PUBLIC_PREFIX in pdf_url:
            idx = pdf_url.index(PUBLIC_PREFIX) + len(PUBLIC_PREFIX)
        elif SIGN_PREFIX in pdf_url:
            idx = pdf_url.index(SIGN_PREFIX) + len(SIGN_PREFIX)
        else:
            return None

        rest = pdf_url[idx:]
        # Remove query string if any
        rest = rest.split("?", 1)[0]
        # First segment is bucket
        parts = rest.split("/", 1)
        if len(parts) != 2:
            return None
        bucket, obj_path = parts[0], parts[1]
        return bucket, obj_path
    except Exception:
        return None


def main() -> int:
    print(f"[INFO] Starting cleanup for announcements before {CUTOFF_DATE.isoformat()}...")
    session = SessionLocal()

    # Fetch candidate rows
    sel_sql = text(
        """
        SELECT id, pdf_url
        FROM announcements
        WHERE publication_date < :cutoff
          AND pdf_url IS NOT NULL
        ORDER BY publication_date ASC
        """
    )

    upd_sql = text(
        """
        UPDATE announcements
        SET pdf_url = NULL,
            newspaper_name = :marker,
            updated_at = NOW()
        WHERE id = :id
        """
    )

    deleted_count = 0
    updated_count = 0
    skipped_count = 0

    try:
        rows = session.execute(sel_sql, {"cutoff": CUTOFF_DATE}).fetchall()
        total = len(rows)
        print(f"[INFO] Found {total} announcement(s) with pre-2021 pdf_url.")

        for (ann_id, pdf_url) in rows:
            if not pdf_url:
                skipped_count += 1
                continue

            parsed = parse_bucket_and_path(pdf_url)
            if not parsed:
                print(f"[WARN] Could not parse storage path from URL: {pdf_url}")
                skipped_count += 1
                # Still clear the column and mark as pre-2021
                session.execute(upd_sql, {"id": ann_id, "marker": MARKER_VALUE})
                updated_count += 1
                continue

            bucket, obj_path = parsed

            try:
                # Delete from Supabase Storage
                res = supabase.storage.from_(bucket).remove([obj_path])
                # Supabase python client returns a list of dicts with 'name' on success, but we won't rely on shape
                print(f"[DEL] Removed {bucket}/{obj_path}")
                deleted_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to remove {bucket}/{obj_path}: {e}")
                # Continue to DB update anyway to maintain consistency with decision

            # Update DB fields
            session.execute(upd_sql, {"id": ann_id, "marker": MARKER_VALUE})
            updated_count += 1

        session.commit()
        print(
            f"[DONE] Deleted files: {deleted_count}, Updated rows: {updated_count}, Skipped: {skipped_count}"
        )
        return 0
    except Exception as e:
        session.rollback()
        print(f"[FATAL] Cleanup failed: {e}")
        return 1
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(main())
