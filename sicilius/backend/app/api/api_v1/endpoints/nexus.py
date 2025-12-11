from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.nexus.graph_service import NexusGraphService
from app.models.company import Company

router = APIRouter()

@router.get("/network/{company_id}", response_model=Dict[str, Any])
def get_company_network_analysis(
    company_id: UUID,
    depth: int = 2,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get graph network analysis for a target company.
    Includes shareholder loops, suspicious address clustering, and contagion risks.
    """
    # 1. Check if company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    # 2. Run Analysis
    try:
        service = NexusGraphService(db)
        result = service.analyze_company_network(company_id, depth=depth, limit=limit)
        return result
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Graph analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Graph analysis failed: {str(e)}"
        )
