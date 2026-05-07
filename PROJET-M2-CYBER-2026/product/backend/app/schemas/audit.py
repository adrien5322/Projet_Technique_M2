"""Pydantic schemas for AuditLog validation."""

from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class AuditLogResponse(BaseModel):
    """Schema for audit log response."""

    id: int
    user_id: Optional[int]
    action: str
    resource_type: str
    resource_id: Optional[str]
    details: Optional[Any]
    ip_address: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """Schema for paginated audit log list response."""

    items: list[AuditLogResponse]
    total: int
    skip: int
    limit: int


class AuditLogCreate(BaseModel):
    """Schema for creating an audit log entry (internal use)."""

    user_id: Optional[int] = None
    action: str = Field(..., max_length=100)
    resource_type: str = Field(..., max_length=50)
    resource_id: Optional[str] = Field(None, max_length=255)
    details: Optional[Any] = None
    ip_address: Optional[str] = Field(None, max_length=45)
