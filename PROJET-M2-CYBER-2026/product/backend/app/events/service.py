"""Events service for security event ingestion and retrieval."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.event import Event
from app.schemas.event import EventCreate


def create_event(db: Session, event_data: EventCreate) -> Event:
    """
    Create a new security event record.

    Args:
        db: Database session
        event_data: Event data to create

    Returns:
        Created Event instance
    """
    db_event = Event(
        source_ip=event_data.source_ip,
        event_type=event_data.event_type,
        severity=event_data.severity,
        raw_data=event_data.raw_data,
        asset_id=event_data.asset_id,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


def get_events(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    severity: Optional[str] = None,
    event_type: Optional[str] = None,
) -> tuple[list[Event], int]:
    """
    Get paginated list of security events with optional filters.

    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        severity: Filter by severity level
        event_type: Filter by event type

    Returns:
        Tuple of (list of Event instances, total count)
    """
    query = db.query(Event)

    if severity:
        query = query.filter(Event.severity == severity)
    if event_type:
        query = query.filter(Event.event_type == event_type)

    total = query.count()

    events = (
        query.order_by(desc(Event.timestamp))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return events, total


def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
    """
    Get a single security event by ID.

    Args:
        db: Database session
        event_id: Event ID to query

    Returns:
        Event instance or None if not found
    """
    return db.query(Event).filter(Event.id == event_id).first()
