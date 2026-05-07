"""Pydantic schemas for Dashboard responses."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DashboardSummaryResponse(BaseModel):
    """Schema for complete dashboard summary response."""

    # Assets
    total_assets: int
    active_assets: int
    inactive_assets: int

    # Events
    total_events: int
    events_by_severity: dict[str, int]
    events_by_type: dict[str, int]

    # Alerts
    total_alerts: int
    alerts_by_status: dict[str, int]
    alerts_by_severity: dict[str, int]

    # Correlations
    total_correlations: int
    open_correlations: int

    # Recent items
    recent_events: list[dict]
    recent_alerts: list[dict]


class TopAttackerResponse(BaseModel):
    """Schema for top attacker IP response."""

    ip: str
    event_count: int
    severity_score: int
    event_types: list[str]
    first_seen: datetime
    last_seen: datetime


class ActivityTimelineResponse(BaseModel):
    """Schema for activity timeline response."""

    hour: datetime
    event_count: int
    alert_count: int
