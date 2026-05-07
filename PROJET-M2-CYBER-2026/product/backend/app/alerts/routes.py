"""Alert routes for security alert management."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session

from app.auth.dependencies import get_db, require_admin, require_analyst_or_admin
from app.models.user import User
from app.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertAssign,
    AlertResponse,
    AlertListResponse,
    AlertStatsResponse,
)
from app.alerts import service as alert_service
from app.audit import service as audit_service

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new alert",
)
async def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
    request: Request = None,
) -> AlertResponse:
    """
    Create a new security alert.

    Requires **admin** role.
    """
    alert = alert_service.create_alert(db, alert_data)

    # Audit trail
    client_ip = request.client.host if request and request.client else None
    audit_service.log_action(
        db=db,
        action="alert_created",
        resource_type="alert",
        resource_id=str(alert.id),
        user_id=current_user.id,
        details={"title": alert.title, "severity": alert.severity},
        ip_address=client_ip,
    )

    return AlertResponse.model_validate(alert)


@router.get(
    "",
    response_model=AlertListResponse,
    summary="List alerts with filters",
)
async def list_alerts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Maximum records to return"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    severity_filter: Optional[str] = Query(None, description="Filter by severity"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> AlertListResponse:
    """
    List alerts with pagination and optional filters.

    Requires **analyst** or **admin** role.
    """
    items, total = alert_service.get_alerts(
        db=db,
        skip=skip,
        limit=limit,
        status_filter=status_filter,
        severity_filter=severity_filter,
    )
    return AlertListResponse(
        items=[AlertResponse.model_validate(a) for a in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/stats",
    response_model=AlertStatsResponse,
    summary="Get alert statistics",
)
async def get_alert_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> AlertStatsResponse:
    """
    Get alert statistics grouped by status and severity.

    Requires **analyst** or **admin** role.
    """
    stats = alert_service.get_alert_stats(db)
    return AlertStatsResponse(**stats)


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
    summary="Get alert details",
)
async def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> AlertResponse:
    """
    Get details of a specific alert.

    Requires **analyst** or **admin** role.
    """
    alert = alert_service.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    return AlertResponse.model_validate(alert)


@router.patch(
    "/{alert_id}/status",
    response_model=AlertResponse,
    summary="Update alert status",
)
async def update_alert_status(
    alert_id: int,
    update_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
    request: Request = None,
) -> AlertResponse:
    """
    Update the status of an alert.

    Requires **analyst** or **admin** role.
    """
    alert = alert_service.update_alert_status(db, alert_id, update_data.status.value)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    # Audit trail
    client_ip = request.client.host if request and request.client else None
    audit_service.log_action(
        db=db,
        action="alert_status_updated",
        resource_type="alert",
        resource_id=str(alert_id),
        user_id=current_user.id,
        details={"new_status": update_data.status.value},
        ip_address=client_ip,
    )

    return AlertResponse.model_validate(alert)


@router.post(
    "/{alert_id}/assign",
    response_model=AlertResponse,
    summary="Assign an alert to an analyst",
)
async def assign_alert_route(
    alert_id: int,
    assign_data: AlertAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
    request: Request = None,
) -> AlertResponse:
    """
    Assign an alert to an analyst.

    Requires **admin** role.

    The assigned user must have an 'analyst' or 'admin' role.
    """
    try:
        alert = alert_service.assign_alert(db, alert_id, assign_data.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    # Audit trail
    client_ip = request.client.host if request and request.client else None
    audit_service.log_action(
        db=db,
        action="alert_assigned",
        resource_type="alert",
        resource_id=str(alert_id),
        user_id=current_user.id,
        details={"assigned_to": assign_data.user_id},
        ip_address=client_ip,
    )

    return AlertResponse.model_validate(alert)
