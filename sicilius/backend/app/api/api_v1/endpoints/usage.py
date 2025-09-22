from datetime import datetime
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app import models

router = APIRouter()


def _limit_from_env() -> int:
    try:
        return int(os.getenv("TSG_DAILY_QUERY_LIMIT", "20"))
    except Exception:
        return 20


@router.get("/me", summary="Get today's usage and remaining queries for current user")
def my_usage(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    today = datetime.utcnow().date()
    usage = (
        db.query(models.DailyUsage)
        .filter(models.DailyUsage.user_id == current_user.id, models.DailyUsage.day == today)
        .first()
    )
    limit = _limit_from_env()
    count = usage.count if usage else 0
    remaining = max(0, limit - count)
    return {
        "date": str(today),
        "count": int(count),
        "limit": int(limit),
        "remaining": int(remaining),
    }
