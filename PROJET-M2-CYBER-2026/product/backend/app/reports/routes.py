"""Reports routes for data export (CSV, JSON).

Provides endpoints to export alerts, events, audit logs, and assets
in CSV or JSON format. Requires authentication and appropriate role.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_admin, require_analyst_or_admin
from app.db import get_db
from app.models.user import User
from app.reports.service import generate_csv, generate_json, get_export_data

router = APIRouter(prefix="/api/v1/export", tags=["reports"])


def _export_response(content: str, filename: str, media_type: str) -> Response:
    """Build a file-download Response with proper headers."""
    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


# ---------------------------------------------------------------------------
# Alerts exports
# ---------------------------------------------------------------------------

@router.get("/alerts/csv")
async def export_alerts_csv(
    from_date: Optional[str] = Query(None, description="Start date (ISO 8601: YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (ISO 8601: YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> Response:
    """Export alerts as CSV with optional date filtering. Requires analyst or admin role."""
    data = get_export_data(db, "alerts", from_date=from_date, to_date=to_date)
    content, filename = generate_csv(data, "alerts")
    return _export_response(content, filename, "text/csv")


@router.get("/alerts/json")
async def export_alerts_json(
    from_date: Optional[str] = Query(None, description="Start date (ISO 8601: YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (ISO 8601: YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> Response:
    """Export alerts as JSON with optional date filtering. Requires analyst or admin role."""
    data = get_export_data(db, "alerts", from_date=from_date, to_date=to_date)
    content, filename = generate_json(data, "alerts")
    return _export_response(content, filename, "application/json")


# ---------------------------------------------------------------------------
# Events exports
# ---------------------------------------------------------------------------

@router.get("/events/csv")
async def export_events_csv(
    from_date: Optional[str] = Query(None, description="Start date (ISO 8601: YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (ISO 8601: YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> Response:
    """Export events as CSV with optional date filtering. Requires analyst or admin role."""
    data = get_export_data(db, "events", from_date=from_date, to_date=to_date)
    content, filename = generate_csv(data, "events")
    return _export_response(content, filename, "text/csv")


@router.get("/events/json")
async def export_events_json(
    from_date: Optional[str] = Query(None, description="Start date (ISO 8601: YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (ISO 8601: YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> Response:
    """Export events as JSON with optional date filtering. Requires analyst or admin role."""
    data = get_export_data(db, "events", from_date=from_date, to_date=to_date)
    content, filename = generate_json(data, "events")
    return _export_response(content, filename, "application/json")


# ---------------------------------------------------------------------------
# Audit logs exports (admin only)
# ---------------------------------------------------------------------------

@router.get("/audit/csv")
async def export_audit_csv(
    from_date: Optional[str] = Query(None, description="Start date (ISO 8601: YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (ISO 8601: YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Response:
    """Export audit logs as CSV with optional date filtering. Requires admin role."""
    data = get_export_data(db, "audit", from_date=from_date, to_date=to_date)
    content, filename = generate_csv(data, "audit")
    return _export_response(content, filename, "text/csv")


@router.get("/audit/json")
async def export_audit_json(
    from_date: Optional[str] = Query(None, description="Start date (ISO 8601: YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (ISO 8601: YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> Response:
    """Export audit logs as JSON with optional date filtering. Requires admin role."""
    data = get_export_data(db, "audit", from_date=from_date, to_date=to_date)
    content, filename = generate_json(data, "audit")
    return _export_response(content, filename, "application/json")


# ---------------------------------------------------------------------------
# Assets exports
# ---------------------------------------------------------------------------

@router.get("/assets/csv")
async def export_assets_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> Response:
    """Export all assets as CSV. Requires analyst or admin role."""
    data = get_export_data(db, "assets")
    content, filename = generate_csv(data, "assets")
    return _export_response(content, filename, "text/csv")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

@router.get("/summary")
async def export_summary(
    from_date: Optional[str] = Query(None, description="Start date (ISO 8601: YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (ISO 8601: YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> dict:
    """Return a global summary with counts for each exportable entity.

    Supports optional date filtering. Requires analyst or admin role.
    """
    summary = {}
    for entity_type in ["alerts", "events", "audit", "assets"]:
        data = get_export_data(db, entity_type, from_date=from_date, to_date=to_date)
        summary[entity_type] = {
            "count": len(data),
            "exportable": True,
        }

    return {
        "summary": summary,
        "generated_by": current_user.username,
    }
