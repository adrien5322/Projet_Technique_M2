"""Dashboard routes for SOC dashboard and visualization."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_db, require_analyst_or_admin
from app.models.user import User
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    TopAttackerResponse,
    ActivityTimelineResponse,
)
from app.dashboard import service as dashboard_service

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Get dashboard summary",
)
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> DashboardSummaryResponse:
    """
    Get complete dashboard summary with counts and recent items.

    Requires **analyst** or **admin** role.

    Returns:
    - Asset statistics (total, active, inactive)
    - Event statistics (total, by severity, by type)
    - Alert statistics (total, by status, by severity)
    - Correlation statistics (total, open)
    - Recent events (last 10)
    - Recent alerts (last 10)
    """
    summary = dashboard_service.get_dashboard_summary(db)
    return DashboardSummaryResponse(**summary)


@router.get(
    "/attackers",
    response_model=list[TopAttackerResponse],
    summary="Get top attacking IPs",
)
async def get_top_attackers(
    limit: int = Query(20, ge=1, le=100, description="Number of top attackers to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> list[TopAttackerResponse]:
    """
    Get top attacker IPs based on threat score.

    Requires **analyst** or **admin** role.

    The threat score is calculated as:
    score = event_count * severity_weight (critical=4, high=3, medium=2, low=1)

    Returns top N IPs sorted by threat score descending.
    """
    attackers = dashboard_service.get_top_attackers(db, limit=limit)
    return [TopAttackerResponse(**attacker) for attacker in attackers]


@router.get(
    "/activity",
    response_model=list[ActivityTimelineResponse],
    summary="Get activity timeline",
)
async def get_activity_timeline(
    hours: int = Query(24, ge=1, le=168, description="Number of hours to look back"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> list[ActivityTimelineResponse]:
    """
    Get activity timeline grouped by hour.

    Requires **analyst** or **admin** role.

    Returns event and alert counts grouped by hour for the last N hours.
    Maximum 168 hours (7 days) allowed.
    """
    timeline = dashboard_service.get_activity_timeline(db, hours=hours)
    return [ActivityTimelineResponse(**item) for item in timeline]
