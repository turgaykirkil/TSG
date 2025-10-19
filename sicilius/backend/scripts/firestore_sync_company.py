#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.core.config import settings
from app.core.search_tokens import tokenize_for_search
from app.core.firebase import get_firestore_client


def _get_engine() -> Engine:
    return create_engine(str(settings.DATABASE_URL))


def fetch_company(company_id: str) -> Optional[Dict[str, Any]]:
    engine = _get_engine()
    sql = text(
        """
        SELECT id, unvan, address, city, district, sicil_no, mersis_number
        FROM app.companies
        WHERE id = :cid
        """
    )
    with engine.connect() as conn:
        row = conn.execute(sql, {"cid": company_id}).mappings().first()
        if not row:
            return None
        return dict(row)


def build_company_doc(row: Dict[str, Any]) -> Dict[str, Any]:
    unvan = (row.get("unvan") or "").strip()
    address = (row.get("address") or row.get("adres") or "").strip()
    city = (row.get("city") or "").strip()
    district = (row.get("district") or "").strip()
    sicil_no = (row.get("sicil_no") or "").strip()
    mersis_number_masked = (row.get("mersis_number") or "").strip()

    doc = {
        "unvan": unvan or None,
        "address": address or None,
        "city": city or None,
        "district": district or None,
        "sicil_no": sicil_no or None,
        "mersis_number_masked": mersis_number_masked or None,
        # Basit token alanları (Firestore arama için)
        "search_tokens_unvan": tokenize_for_search(unvan, max_tokens=20),
        "search_tokens_address": tokenize_for_search(address, max_tokens=20),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    return doc


def upsert_company(company_id: str, dry_run: bool = False) -> Dict[str, Any]:
    row = fetch_company(company_id)
    if not row:
        raise SystemExit(f"Company not found: {company_id}")
    doc = build_company_doc(row)

    if dry_run:
        print(json.dumps({"id": company_id, **doc}, ensure_ascii=False, indent=2))
        return doc

    db = get_firestore_client()
    db.collection("companies").document(company_id).set(doc, merge=True)
    return doc


def main():
    load_dotenv()  # ensure .env is loaded

    parser = argparse.ArgumentParser(description="Sync a single company to Firestore")
    parser.add_argument("--id", required=True, help="Company UUID to sync")
    parser.add_argument("--dry-run", action="store_true", help="Print doc without writing to Firestore")
    args = parser.parse_args()

    doc = upsert_company(args.id, dry_run=args.dry_run)
    if not args.dry_run:
        print(json.dumps({"ok": True, "id": args.id, "wrote": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
