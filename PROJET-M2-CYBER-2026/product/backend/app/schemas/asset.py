"""Pydantic schemas for Asset validation."""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator, IPvAnyAddress
from enum import Enum


class AssetType(str, Enum):
    """Valid asset types."""
    SERVER = "server"
    WORKSTATION = "workstation"
    LAPTOP = "laptop"
    MOBILE = "mobile"
    IOT = "iot"


class AssetStatus(str, Enum):
    """Valid asset statuses."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class AssetBase(BaseModel):
    """Base asset schema with common fields."""
    
    hostname: str = Field(..., min_length=1, max_length=255, description="Asset hostname")
    ip_address: Optional[str] = Field(None, description="IP address (IPv4 or IPv6)")
    mac_address: Optional[str] = Field(None, description="MAC address (XX:XX:XX:XX:XX:XX)")
    asset_type: AssetType = Field(..., description="Asset type")
    os_type: Optional[str] = Field(None, max_length=50, description="Operating system type")
    os_version: Optional[str] = Field(None, max_length=100, description="OS version")
    status: AssetStatus = Field(AssetStatus.ACTIVE, description="Asset status")
    tags: Optional[Dict[str, Any]] = Field(None, description="Tags as key-value pairs")
    
    @validator('ip_address')
    def validate_ip_address(cls, v: Optional[str]) -> Optional[str]:
        """Validate IP address format."""
        if v is None:
            return v
        try:
            IPvAnyAddress(v)
        except Exception:
            raise ValueError('Invalid IP address format')
        return v
    
    @validator('mac_address')
    def validate_mac_address(cls, v: Optional[str]) -> Optional[str]:
        """Validate MAC address format."""
        if v is None:
            return v
        # Accept common MAC address formats
        import re
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if not mac_pattern.match(v):
            raise ValueError('Invalid MAC address format. Use XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX')
        return v.upper()  # Normalize to uppercase


class AssetCreate(AssetBase):
    """Schema for creating a new asset."""
    pass


class AssetUpdate(BaseModel):
    """Schema for updating an existing asset (all fields optional)."""
    
    hostname: Optional[str] = Field(None, min_length=1, max_length=255)
    ip_address: Optional[str] = Field(None)
    mac_address: Optional[str] = Field(None)
    asset_type: Optional[AssetType] = None
    os_type: Optional[str] = Field(None, max_length=50)
    os_version: Optional[str] = Field(None, max_length=100)
    status: Optional[AssetStatus] = None
    tags: Optional[Dict[str, Any]] = None
    
    @validator('ip_address')
    def validate_ip_address(cls, v: Optional[str]) -> Optional[str]:
        """Validate IP address format."""
        if v is None:
            return v
        try:
            IPvAnyAddress(v)
        except Exception:
            raise ValueError('Invalid IP address format')
        return v
    
    @validator('mac_address')
    def validate_mac_address(cls, v: Optional[str]) -> Optional[str]:
        """Validate MAC address format."""
        if v is None:
            return v
        import re
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if not mac_pattern.match(v):
            raise ValueError('Invalid MAC address format. Use XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX')
        return v.upper()


class AssetResponse(AssetBase):
    """Schema for asset response."""
    
    id: int
    last_seen: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class AssetListResponse(BaseModel):
    """Schema for paginated asset list response."""
    
    items: list[AssetResponse]
    total: int
    skip: int
    limit: int
