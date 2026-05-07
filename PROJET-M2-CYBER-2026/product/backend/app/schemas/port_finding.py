"""Pydantic schemas for PortFinding validation."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class Protocol(str, Enum):
    """Valid network protocols."""
    TCP = "tcp"
    UDP = "udp"


class PortState(str, Enum):
    """Valid port states."""
    OPEN = "open"
    CLOSED = "closed"
    FILTERED = "filtered"


class PortFindingCreate(BaseModel):
    """Schema for creating a port finding."""

    asset_id: int = Field(..., description="ID of the associated asset")
    port: int = Field(..., ge=1, le=65535, description="Port number (1-65535)")
    protocol: Protocol = Field(Protocol.TCP, description="Network protocol")
    service_name: str = Field(..., min_length=1, max_length=100, description="Detected service name")
    state: PortState = Field(PortState.OPEN, description="Port state")


class PortFindingResponse(BaseModel):
    """Schema for port finding response."""

    id: int
    asset_id: int
    port: int
    protocol: str
    service_name: str
    service_version: Optional[str]
    state: str
    discovered_at: datetime

    class Config:
        from_attributes = True


class PortFindingListResponse(BaseModel):
    """Schema for paginated port finding list response."""

    items: list[PortFindingResponse]
    total: int
    skip: int
    limit: int
