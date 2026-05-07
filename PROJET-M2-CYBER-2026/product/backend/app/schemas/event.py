"""Pydantic schemas for Event validation."""

from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


VALID_EVENT_TYPES = [
    "network_scan",
    "brute_force",
    "malware",
    "unauthorized_access",
    "data_exfiltration",
    "other",
]

VALID_SEVERITIES = ["low", "medium", "high", "critical"]


class EventBase(BaseModel):
    """Base event schema."""

    source_ip: Optional[str] = Field(None, max_length=45, description="Source IP address (IPv4 or IPv6)")
    event_type: str = Field(..., description=f"Event type: {', '.join(VALID_EVENT_TYPES)}")
    severity: str = Field(..., description=f"Severity level: {', '.join(VALID_SEVERITIES)}")
    raw_data: Optional[dict[str, Any]] = Field(None, description="Raw event data as JSON")
    asset_id: Optional[int] = Field(None, description="Associated asset ID")

    @validator("event_type")
    def validate_event_type(cls, v: str) -> str:
        """Validate event_type value."""
        if v not in VALID_EVENT_TYPES:
            raise ValueError(f"Event type must be one of: {', '.join(VALID_EVENT_TYPES)}")
        return v

    @validator("severity")
    def validate_severity(cls, v: str) -> str:
        """Validate severity value."""
        if v not in VALID_SEVERITIES:
            raise ValueError(f"Severity must be one of: {', '.join(VALID_SEVERITIES)}")
        return v


class EventCreate(EventBase):
    """Schema for creating a new event."""
    pass


class EventResponse(EventBase):
    """Schema for event response."""

    id: int
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Schema for paginated event list response."""

    events: list[EventResponse]
    total: int
    page: int
    page_size: int
