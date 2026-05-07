"""Events routes for security event ingestion."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.auth.dependencies import require_analyst_or_admin, verify_agent_or_user, rate_limit_agent
from app.models.user import User
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse, EventListResponse
from app.events.service import create_event, get_events, get_event_by_id

router = APIRouter(prefix="/api/v1/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def ingest_event(
    event_data: EventCreate,
    request: Request,
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(rate_limit_agent),
    auth=Depends(verify_agent_or_user),
) -> Event:
    """
    Ingest a new security event.

    Accepts authentication via:
    - JWT Bearer token (analyst or admin role)
    - X-Agent-Secret header (agent authentication)

    - **source_ip**: Source IP address (optional)
    - **event_type**: Type of security event
    - **severity**: Severity level (low, medium, high, critical)
    - **raw_data**: Raw event data as JSON (optional)
    - **asset_id**: Associated asset ID (optional)
    """
    return create_event(db, event_data)


@router.get("", response_model=EventListResponse)
async def list_events(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> dict:
    """
    List security events with pagination and filters.

    Requires analyst or admin role.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 50, max: 200)
    - **severity**: Filter by severity level
    - **event_type**: Filter by event type
    """
    skip = (page - 1) * page_size
    events, total = get_events(
        db,
        skip=skip,
        limit=page_size,
        severity=severity,
        event_type=event_type,
    )

    return {
        "events": events,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> Event:
    """
    Get a specific security event by ID.

    Requires analyst or admin role.

    - **event_id**: Event ID to retrieve
    """
    event = get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event
