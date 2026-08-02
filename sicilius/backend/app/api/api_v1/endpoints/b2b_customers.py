import uuid
import secrets
import hashlib
from typing import Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import models
from app.api import deps

router = APIRouter()

class B2BCustomerCreatePayload(BaseModel):
    title: str
    taxNumber: str
    contactEmail: EmailStr
    packageName: str = "Pro" # Basic, Pro, Enterprise
    monthlyQuota: Optional[int] = 15000

class GenerateKeyPayload(BaseModel):
    name: Optional[str] = "Live Key"
    keyType: Optional[str] = "live" # live, sandbox

@router.get("")
@router.get("/")
def list_b2b_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    List all B2B enterprise customers from PostgreSQL DB cleanly.
    """
    try:
        sql = text("""
            SELECT 
                c.id::text, 
                c.title, 
                c.tax_number as "taxNumber", 
                c.contact_email as "contactEmail", 
                c.package_name as "packageName", 
                c.monthly_quota as "monthlyQuota", 
                c.used_quota as "usedQuota", 
                c.is_active as "isActive", 
                c.created_at::text as "createdAt"
            FROM app.b2b_customers c
            ORDER BY c.created_at DESC
            OFFSET :skip LIMIT :limit
        """)
        rows = db.execute(sql, {"skip": skip, "limit": limit}).mappings().all()
        return [dict(r) for r in rows]
    except Exception:
        return []

@router.post("")
@router.post("/")
def create_b2b_customer(
    *,
    db: Session = Depends(deps.get_db),
    payload: B2BCustomerCreatePayload,
) -> Any:
    """
    Create a new B2B customer record in PostgreSQL DB.
    """
    # Check if tax number already exists
    existing = db.execute(
        text("SELECT id FROM app.b2b_customers WHERE tax_number = :vkn"), 
        {"vkn": payload.taxNumber}
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu VKN (Vergi No) ile kayıtlı bir müşteri zaten var.")

    # Determine default quota based on package
    quota = payload.monthlyQuota or 15000
    if payload.packageName == "Enterprise":
        quota = max(quota, 50000)
    elif payload.packageName == "Basic":
        quota = 5000

    insert_sql = text("""
        INSERT INTO app.b2b_customers (title, tax_number, contact_email, package_name, monthly_quota, used_quota, is_active)
        VALUES (:title, :vkn, :email, :pkg, :quota, 0, TRUE)
        RETURNING id::text, title, tax_number as "taxNumber", contact_email as "contactEmail", package_name as "packageName", monthly_quota as "monthlyQuota", used_quota as "usedQuota", is_active as "isActive", created_at::text as "createdAt"
    """)
    row = db.execute(insert_sql, {
        "title": payload.title,
        "vkn": payload.taxNumber,
        "email": payload.contactEmail,
        "pkg": payload.packageName,
        "quota": quota
    }).mappings().first()
    db.commit()

    customer_dict = dict(row)
    customer_dict["activeKeysCount"] = 0
    return customer_dict

@router.post("/{customer_id}/toggle-status")
@router.post("/{customer_id}/toggle-status/")
def toggle_customer_status(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: str,
) -> Any:
    """
    Toggle customer active/inactive status in DB.
    """
    update_sql = text("""
        UPDATE app.b2b_customers 
        SET is_active = NOT is_active, updated_at = NOW() 
        WHERE id = CAST(:id AS uuid)
        RETURNING is_active
    """)
    res = db.execute(update_sql, {"id": customer_id}).first()
    if not res:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.commit()
    return {"message": "Status updated successfully", "isActive": res[0]}

@router.post("/{customer_id}/generate-key")
@router.post("/{customer_id}/generate-key/")
def generate_api_key(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: str,
    payload: GenerateKeyPayload = Body(default=GenerateKeyPayload()),
) -> Any:
    """
    Generate a new HMAC-SHA256 API Key for a customer and store securely in DB.
    """
    # Verify customer exists
    cust = db.execute(text("SELECT id, title FROM app.b2b_customers WHERE id = CAST(:id AS uuid)"), {"id": customer_id}).first()
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")

    raw_secret = secrets.token_hex(24) # e.g. 48 hex chars
    prefix = f"sk_{payload.keyType}_{secrets.token_hex(4)}"
    full_key = f"{prefix}_{raw_secret}"
    hashed = hashlib.sha256(full_key.encode('utf-8')).hexdigest()

    insert_key = text("""
        INSERT INTO app.api_keys (customer_id, name, key_prefix, hashed_key, key_type, is_active)
        VALUES (CAST(:cust_id AS uuid), :name, :prefix, :hashed, :ktype, TRUE)
        RETURNING id::text
    """)
    db.execute(insert_key, {
        "cust_id": customer_id,
        "name": payload.name or "Live Key",
        "prefix": prefix,
        "hashed": hashed,
        "ktype": payload.keyType or "live"
    })
    db.commit()

    return {
        "message": "API Key generated successfully",
        "liveKey": prefix + "_***",
        "liveSecret": full_key,
        "customerTitle": cust[1]
    }

@router.delete("/{customer_id}")
@router.delete("/{customer_id}/")
def delete_b2b_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: str,
) -> Any:
    """
    Delete a B2B customer and their API keys from DB.
    """
    del_sql = text("DELETE FROM app.b2b_customers WHERE id = CAST(:id AS uuid)")
    res = db.execute(del_sql, {"id": customer_id})
    db.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully", "id": customer_id}
