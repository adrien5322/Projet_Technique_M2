"""Pydantic schemas for Alert validation."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class AlertSeverity(str, Enum):
    """Valid alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Valid alert statuses."""
    NEW = "new"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


class AlertCreate(BaseModel):
    """Schema for creating a new alert."""

    title: str = Field(..., min_length=1, max_length=255, description="Alert title")
    description: str = Field(..., min_length=1, max_length=2000, description="Alert description")
    severity: AlertSeverity = Field(..., description="Alert severity level")
    source_event_id: Optional[str] = Field(None, max_length=255, description="Source event identifier")


class AlertUpdate(BaseModel):
    """Schema for updating an existing alert (all fields optional for PATCH)."""

    status: Optional[AlertStatus] = None
    assigned_to: Optional[int] = None


class AlertResponse(BaseModel):
    """Schema for alert response."""

    id: int
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    source_event_id: Optional[str]
    assigned_to: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    """Schema for paginated alert list response."""

    items: list[AlertResponse]
    total: int
    skip: int
    limit: int


class AlertAssign(BaseModel):
    """Schema for assigning an alert to an analyst."""

    user_id: int = Field(..., gt=0, description="ID of the analyst to assign")


class AlertStatsResponse(BaseModel):
    """Schema for alert statistics response."""

    by_status: dict[str, int]
    by_severity: dict[str, int]
    total: int
