"""Correlation schemas for request/response validation."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class CorrelationGroupCreate(BaseModel):
    """Schema for creating a correlation group."""
    
    rule_type: str
    rule_key: str
    severity: str = "medium"
    score: int = 0
    description: Optional[str] = None


class CorrelatedEventSummary(BaseModel):
    """Schema for event summary within a correlation group."""
    
    id: int
    source_ip: str
    event_type: str
    severity: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class CorrelationGroupResponse(BaseModel):
    """Schema for correlation group response with events."""
    
    id: int
    rule_type: str
    rule_key: str
    severity: str
    score: int
    event_count: int
    first_seen: datetime
    last_seen: datetime
    status: str
    assigned_to: Optional[int]
    description: Optional[str]
    events: List[CorrelatedEventSummary]
    
    class Config:
        from_attributes = True


class CorrelationGroupListResponse(BaseModel):
    """Schema for paginated correlation group list."""
    
    items: List[CorrelationGroupResponse]
    total: int
    skip: int
    limit: int


class CorrelationGroupUpdate(BaseModel):
    """Schema for updating a correlation group."""
    
    status: Optional[str] = None
    assigned_to: Optional[int] = None


class CorrelationStatsResponse(BaseModel):
    """Schema for correlation statistics."""
    
    total_groups: int
    by_rule_type: dict[str, int]
    by_status: dict[str, int]
    by_severity: dict[str, int]
    open_groups: int
    investigating_groups: int
    resolved_groups: int
    false_positive_groups: int
