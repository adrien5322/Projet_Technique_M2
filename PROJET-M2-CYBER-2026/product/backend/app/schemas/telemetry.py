"""Pydantic schemas for Telemetry validation."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class TelemetryHeartbeatBase(BaseModel):
    """Base telemetry heartbeat schema."""
    
    asset_id: Optional[int] = Field(None, description="Asset ID (optional for now, will be required in EPIC-03)")
    status: str = Field(..., description="Asset status: online, offline, or warning")
    cpu_usage: Optional[float] = Field(None, ge=0.0, le=100.0, description="CPU usage percentage (0-100)")
    memory_usage: Optional[float] = Field(None, ge=0.0, le=100.0, description="Memory usage percentage (0-100)")
    disk_usage: Optional[float] = Field(None, ge=0.0, le=100.0, description="Disk usage percentage (0-100)")
    network_latency: Optional[float] = Field(None, ge=0.0, description="Network latency in milliseconds")
    
    @validator('status')
    def validate_status(cls, v: str) -> str:
        """Validate status value."""
        valid_statuses = ['online', 'offline', 'warning']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v


class TelemetryHeartbeatCreate(TelemetryHeartbeatBase):
    """Schema for creating a new heartbeat."""
    pass


class TelemetryHeartbeatResponse(TelemetryHeartbeatBase):
    """Schema for heartbeat response."""
    
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class TelemetryStatusSummary(BaseModel):
    """Schema for overall telemetry status summary."""
    
    total_assets: int = Field(..., description="Total number of assets with heartbeats")
    online_count: int = Field(..., description="Number of online assets")
    offline_count: int = Field(..., description="Number of offline assets")
    warning_count: int = Field(..., description="Number of assets in warning state")
    missed_heartbeats_count: int = Field(..., description="Number of assets that missed heartbeat")


class MissedHeartbeatInfo(BaseModel):
    """Schema for missed heartbeat information."""
    
    asset_id: int
    last_heartbeat: Optional[datetime]
    minutes_since_last: Optional[float]
