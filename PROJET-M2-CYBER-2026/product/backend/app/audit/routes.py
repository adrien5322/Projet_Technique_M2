"""Audit routes for audit trail management."""

from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_db, require_admin, verify_agent_secret, rate_limit_agent
from app.models.user import User
from app.schemas.audit import (
    AuditLogResponse,
    AuditLogListResponse,
    AuditLogCreate,
)
from app.audit import service as audit_service

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])


@router.get(
    "/logs",
    response_model=AuditLogListResponse,
    summary="List audit logs",
)
async def list_audit_logs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=200, description="Maximum records to return"),
    action_filter: Optional[str] = Query(None, description="Filter by action type"),
    user_id_filter: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> AuditLogListResponse:
    """
    List audit log entries with pagination and optional filters.

    Requires **admin** role.
    """
    items, total = audit_service.get_audit_logs(
        db=db,
        skip=skip,
        limit=limit,
        action_filter=action_filter,
        user_id_filter=user_id_filter,
    )
    return AuditLogListResponse(
        items=[AuditLogResponse.model_validate(log) for log in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post(
    "/log",
    response_model=AuditLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an audit log entry (internal)",
)
async def create_audit_log(
    log_data: AuditLogCreate,
    request: Request,
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(rate_limit_agent),
    _: bool = Depends(verify_agent_secret),
) -> AuditLogResponse:
    """
    Create an audit log entry.

    This endpoint is intended for internal service-to-service logging.
    Requires a valid `X-Agent-Secret` header.
    """
    # Use request IP if not provided in payload
    ip_address = log_data.ip_address
    if not ip_address and request and request.client:
        ip_address = request.client.host

    audit_entry = audit_service.log_action(
        db=db,
        action=log_data.action,
        resource_type=log_data.resource_type,
        resource_id=log_data.resource_id,
        user_id=log_data.user_id,
        details=log_data.details,
        ip_address=ip_address,
    )
    return AuditLogResponse.model_validate(audit_entry)
