"""Audit service for logging and retrieving audit trail entries."""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.audit import AuditLog


def log_action(
    db: Session,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    user_id: Optional[int] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None,
) -> AuditLog:
    """
    Log a security-relevant action in the audit trail.

    Args:
        db: Database session.
        action: Action performed (e.g. "alert_created", "user_login").
        resource_type: Type of resource affected (e.g. "alert", "user").
        resource_id: Identifier of the specific resource.
        user_id: ID of the user who performed the action.
        details: Additional JSON-serializable details.
        ip_address: IP address of the request.

    Returns:
        The created AuditLog instance.
    """
    audit_entry = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return audit_entry


def get_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    action_filter: Optional[str] = None,
    user_id_filter: Optional[int] = None,
) -> tuple[list[AuditLog], int]:
    """
    Get a paginated list of audit logs with optional filters.

    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        action_filter: Filter by action type.
        user_id_filter: Filter by user ID.

    Returns:
        Tuple of (list of audit logs, total count).
    """
    query = db.query(AuditLog)

    if action_filter:
        query = query.filter(AuditLog.action == action_filter)
    if user_id_filter is not None:
        query = query.filter(AuditLog.user_id == user_id_filter)

    total = query.count()
    items = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()

    return items, total
