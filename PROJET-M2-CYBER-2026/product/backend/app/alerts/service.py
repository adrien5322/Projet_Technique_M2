"""Alert service for business logic."""

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func

from app.models.alert import Alert
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertSeverity, AlertStatus


def create_alert(db: Session, alert_data: AlertCreate) -> Alert:
    """
    Create a new alert.

    Args:
        db: Database session.
        alert_data: Pydantic schema with alert data.

    Returns:
        The created Alert model instance.
    """
    db_alert = Alert(
        title=alert_data.title,
        description=alert_data.description,
        severity=alert_data.severity.value,
        source_event_id=alert_data.source_event_id,
        status="new",
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alert(db: Session, alert_id: int) -> Optional[Alert]:
    """
    Get a single alert by ID.

    Args:
        db: Database session.
        alert_id: Alert ID.

    Returns:
        Alert instance or None if not found.
    """
    return db.query(Alert).filter(Alert.id == alert_id).first()


def get_alerts(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    status_filter: Optional[str] = None,
    severity_filter: Optional[str] = None,
) -> tuple[list[Alert], int]:
    """
    Get a paginated list of alerts with optional filters.

    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        status_filter: Filter by alert status.
        severity_filter: Filter by alert severity.

    Returns:
        Tuple of (list of alerts, total count).
    """
    query = db.query(Alert)

    if status_filter:
        query = query.filter(Alert.status == status_filter)
    if severity_filter:
        query = query.filter(Alert.severity == severity_filter)

    total = query.count()
    items = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()

    return items, total


def update_alert_status(
    db: Session,
    alert_id: int,
    status: str,
) -> Optional[Alert]:
    """
    Update the status of an alert.

    Automatically sets resolved_at when status becomes 'resolved' or 'false_positive'.

    Args:
        db: Database session.
        alert_id: Alert ID.
        status: New status value.

    Returns:
        Updated Alert instance or None if not found.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return None

    alert.status = status
    alert.updated_at = datetime.utcnow()

    if status in ("resolved", "false_positive"):
        alert.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(alert)
    return alert


def get_alert_stats(db: Session) -> dict:
    """
    Get alert statistics grouped by status and severity.

    Args:
        db: Database session.

    Returns:
        Dictionary with counts by status, by severity, and total.
    """
    total = db.query(Alert).count()

    # Count by status
    status_counts = (
        db.query(Alert.status, sa_func.count(Alert.id))
        .group_by(Alert.status)
        .all()
    )
    by_status = {status: count for status, count in status_counts}

    # Count by severity
    severity_counts = (
        db.query(Alert.severity, sa_func.count(Alert.id))
        .group_by(Alert.severity)
        .all()
    )
    by_severity = {severity: count for severity, count in severity_counts}

    return {
        "by_status": by_status,
        "by_severity": by_severity,
        "total": total,
    }


def assign_alert(db: Session, alert_id: int, user_id: int) -> Optional[Alert]:
    """
    Assign an alert to a user (analyst or admin).

    Args:
        db: Database session.
        alert_id: Alert ID.
        user_id: User ID to assign the alert to.

    Returns:
        Updated Alert instance or None if alert not found.

    Raises:
        ValueError: If user doesn't exist or is not an analyst/admin.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return None

    # Verify user exists and has analyst or admin role
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role not in ["analyst", "admin"]:
        raise ValueError("Invalid user or user is not an analyst")

    alert.assigned_to = user_id
    alert.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    return alert
