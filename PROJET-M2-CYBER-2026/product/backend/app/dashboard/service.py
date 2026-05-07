"""Dashboard service for business logic."""

from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict

from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func, and_, desc

from app.models.asset import Asset
from app.models.event import Event
from app.models.alert import Alert
from app.models.correlation import CorrelationGroup


# Severity weights for threat score calculation
SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def get_dashboard_summary(db: Session) -> dict:
    """
    Get complete dashboard summary with counts and recent items.

    Args:
        db: Database session.

    Returns:
        Dictionary with comprehensive dashboard data.
    """
    # Assets statistics
    total_assets = db.query(Asset).count()
    active_assets = db.query(Asset).filter(Asset.status == "active").count()
    inactive_assets = total_assets - active_assets

    # Events statistics
    total_events = db.query(Event).count()

    # Events by severity
    events_severity_counts = (
        db.query(Event.severity, sa_func.count(Event.id))
        .group_by(Event.severity)
        .all()
    )
    events_by_severity = {severity: count for severity, count in events_severity_counts}

    # Events by type
    events_type_counts = (
        db.query(Event.event_type, sa_func.count(Event.id))
        .group_by(Event.event_type)
        .all()
    )
    events_by_type = {event_type: count for event_type, count in events_type_counts}

    # Alerts statistics
    total_alerts = db.query(Alert).count()

    # Alerts by status
    alerts_status_counts = (
        db.query(Alert.status, sa_func.count(Alert.id))
        .group_by(Alert.status)
        .all()
    )
    alerts_by_status = {status: count for status, count in alerts_status_counts}

    # Alerts by severity
    alerts_severity_counts = (
        db.query(Alert.severity, sa_func.count(Alert.id))
        .group_by(Alert.severity)
        .all()
    )
    alerts_by_severity = {severity: count for severity, count in alerts_severity_counts}

    # Correlations statistics
    total_correlations = db.query(CorrelationGroup).count()
    open_correlations = (
        db.query(CorrelationGroup)
        .filter(CorrelationGroup.status == "open")
        .count()
    )

    # Recent events (last 10)
    recent_events = (
        db.query(Event)
        .order_by(desc(Event.timestamp))
        .limit(10)
        .all()
    )
    recent_events_data = [
        {
            "id": event.id,
            "timestamp": event.timestamp,
            "source_ip": event.source_ip,
            "event_type": event.event_type,
            "severity": event.severity,
        }
        for event in recent_events
    ]

    # Recent alerts (last 10)
    recent_alerts = (
        db.query(Alert)
        .order_by(desc(Alert.created_at))
        .limit(10)
        .all()
    )
    recent_alerts_data = [
        {
            "id": alert.id,
            "title": alert.title,
            "severity": alert.severity,
            "status": alert.status,
            "created_at": alert.created_at,
        }
        for alert in recent_alerts
    ]

    return {
        "total_assets": total_assets,
        "active_assets": active_assets,
        "inactive_assets": inactive_assets,
        "total_events": total_events,
        "events_by_severity": events_by_severity,
        "events_by_type": events_by_type,
        "total_alerts": total_alerts,
        "alerts_by_status": alerts_by_status,
        "alerts_by_severity": alerts_by_severity,
        "total_correlations": total_correlations,
        "open_correlations": open_correlations,
        "recent_events": recent_events_data,
        "recent_alerts": recent_alerts_data,
    }


def get_top_attackers(db: Session, limit: int = 20) -> list[dict]:
    """
    Get top attacker IPs based on threat score.

    Args:
        db: Database session.
        limit: Maximum number of attackers to return.

    Returns:
        List of dictionaries with attacker information sorted by threat score.
    """
    # Get all events with source_ip
    events_with_ip = (
        db.query(
            Event.source_ip,
            Event.severity,
            Event.event_type,
            Event.timestamp,
        )
        .filter(Event.source_ip.isnot(None))
        .all()
    )

    # Aggregate by IP
    ip_data: dict[str, dict] = defaultdict(
        lambda: {
            "event_count": 0,
            "severity_score": 0,
            "event_types": set(),
            "first_seen": None,
            "last_seen": None,
        }
    )

    for event in events_with_ip:
        ip = event.source_ip
        data = ip_data[ip]
        data["event_count"] += 1
        data["severity_score"] += SEVERITY_WEIGHTS.get(event.severity, 1)
        data["event_types"].add(event.event_type)

        if data["first_seen"] is None or event.timestamp < data["first_seen"]:
            data["first_seen"] = event.timestamp
        if data["last_seen"] is None or event.timestamp > data["last_seen"]:
            data["last_seen"] = event.timestamp

    # Convert to list and sort by severity_score descending
    attackers = [
        {
            "ip": ip,
            "event_count": data["event_count"],
            "severity_score": data["severity_score"],
            "event_types": list(data["event_types"]),
            "first_seen": data["first_seen"],
            "last_seen": data["last_seen"],
        }
        for ip, data in ip_data.items()
    ]

    attackers.sort(key=lambda x: x["severity_score"], reverse=True)

    return attackers[:limit]


def get_activity_timeline(db: Session, hours: int = 24) -> list[dict]:
    """
    Get activity timeline grouped by hour for the last N hours.

    Args:
        db: Database session.
        hours: Number of hours to look back.

    Returns:
        List of dictionaries with hour, event_count, and alert_count.
    """
    # Calculate the start time
    start_time = datetime.utcnow() - timedelta(hours=hours)

    # Get events grouped by hour
    events_by_hour = (
        db.query(
            sa_func.date_trunc("hour", Event.timestamp).label("hour"),
            sa_func.count(Event.id).label("count"),
        )
        .filter(Event.timestamp >= start_time)
        .group_by(sa_func.date_trunc("hour", Event.timestamp))
        .order_by("hour")
        .all()
    )

    # Get alerts grouped by hour
    alerts_by_hour = (
        db.query(
            sa_func.date_trunc("hour", Alert.created_at).label("hour"),
            sa_func.count(Alert.id).label("count"),
        )
        .filter(Alert.created_at >= start_time)
        .group_by(sa_func.date_trunc("hour", Alert.created_at))
        .order_by("hour")
        .all()
    )

    # Create a dictionary to merge both
    timeline_dict: dict[datetime, dict] = defaultdict(
        lambda: {"event_count": 0, "alert_count": 0}
    )

    for hour, count in events_by_hour:
        timeline_dict[hour]["event_count"] = count

    for hour, count in alerts_by_hour:
        timeline_dict[hour]["alert_count"] = count

    # Convert to list
    timeline = [
        {
            "hour": hour,
            "event_count": data["event_count"],
            "alert_count": data["alert_count"],
        }
        for hour, data in sorted(timeline_dict.items())
    ]

    return timeline
