import math
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import inspection
from pydantic import BaseModel

from app.api.deps import get_db
from app.models.company import Company
from app.models.ocr_result import OcrResult
from app.models.announcement import Announcement
from app.models.person import Person
from app.models.gazette import GazetteEntry

router = APIRouter()

# Register models that the admin can manage
TABLES = {
    "companies": Company,
    "ocr_results": OcrResult,
    "announcements": Announcement,
    "persons": Person,
    "gazette_entries": GazetteEntry
}

def get_model(table_name: str):
    model = TABLES.get(table_name)
    if not model:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
    return model

@router.get("/tables", summary="Get list of available tables")
def list_tables() -> Dict[str, Any]:
    return {
        "tables": [
            {
                "id": k,
                "name": k.replace("_", " ").title()
            } for k in TABLES.keys()
        ]
    }

@router.get("/tables/{table_name}", summary="Get rows from a table")
def get_table_rows(
    table_name: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    model = get_model(table_name)
    query = db.query(model)
    
    # Generic search: try to filter by the first string column
    if search:
        string_columns = [col for col in model.__table__.columns if str(col.type).startswith("VARCHAR") or str(col.type).startswith("TEXT")]
        if string_columns:
            # Search in the first available string column
            target_col = string_columns[0]
            for col in string_columns:
                # Prefer unvan, trade_name, etc. if available
                if "name" in col.name or "unvan" in col.name or "title" in col.name:
                    target_col = col
                    break
            query = query.filter(target_col.ilike(f"%{search}%"))
            total = query.count()
    else:
        # Avoid full table COUNT(*) on large tables which hangs the database
        total = 1000000 # Dummy large number for pagination to work
        
    # Safe order_by
    if hasattr(model, "created_at"):
        query = query.order_by(model.created_at.desc())
        
    items = query.offset((page - 1) * size).limit(size).all()
    
    # Serialize to dict generically
    serialized_items = []
    for item in items:
        data = {}
        for c in item.__table__.columns:
            val = getattr(item, c.name)
            if hasattr(val, 'isoformat'):
                val = val.isoformat()
            data[c.name] = val
        serialized_items.append(data)
        
    return {
        "items": serialized_items,
        "total": total,
        "page": page,
        "size": size,
        "pages": math.ceil(total / size)
    }

@router.put("/tables/{table_name}/{item_id}", summary="Update a row")
def update_table_row(
    table_name: str,
    item_id: str,
    payload: Dict[str, Any],
    db: Session = Depends(get_db)
):
    model = get_model(table_name)
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    for key, value in payload.items():
        if hasattr(item, key):
            setattr(item, key, value)
            
    db.commit()
    db.refresh(item)
    return {"status": "success", "message": "Record updated successfully"}

@router.delete("/tables/{table_name}/{item_id}", summary="Delete a row")
def delete_table_row(
    table_name: str,
    item_id: str,
    db: Session = Depends(get_db)
):
    model = get_model(table_name)
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    db.delete(item)
    db.commit()
    return {"status": "success", "message": "Record deleted successfully"}
