from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.api import deps
from app.api.api_v1.endpoints.processing import process_background_geocoding
from app.models.user import User
from app.nexus.graph_service import NexusGraphService
from app.models.company import Company

router = APIRouter()

@router.get("/network/{company_id}", response_model=Any)
def get_company_network_analysis(
    *,
    db: Session = Depends(deps.get_db),
    company_id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
    limit: int = 50,
    background_tasks: BackgroundTasks
) -> Any:
    """
    Analyze network for a specific company.
    Builds a graph of relationships (Depth 2).
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
        result = service.analyze_company_network(company_id, limit=limit)
        
        # Trigger Background Geocoding for Missing Coordinates
        if result.get('analysis') and result['analysis'].get('missing_coords'):
            background_tasks.add_task(process_background_geocoding, result['analysis']['missing_coords'])
            
        # Trigger Background ML Anomaly Detection
        if result.get('analysis') and result['analysis'].get('ml_features_payload'):
            background_tasks.add_task(service.run_background_anomaly_detection, result['analysis']['ml_features_payload'])
            
        return result
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Graph analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Graph analysis failed: {str(e)}"
        )
