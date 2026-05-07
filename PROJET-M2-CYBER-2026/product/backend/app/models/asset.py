"""Asset model for inventory management."""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.user import Base


class Asset(Base):
    """Asset model representing network assets.
    
    Supports various asset types: server, workstation, laptop, mobile, iot.
    Tracks asset status, OS information, and network identifiers.
    """
    
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(255), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True, index=True)  # IPv6 max length = 45
    mac_address = Column(String(17), nullable=True, index=True)  # XX:XX:XX:XX:XX:XX
    asset_type = Column(String(20), nullable=False, default="server", index=True)
    os_type = Column(String(50), nullable=True)
    os_version = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="active", index=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    tags = Column(JSON, nullable=True)  # Store tags as JSON dictionary
    
    # Relationship to TelemetryHeartbeat (one-to-many)
    heartbeats = relationship("TelemetryHeartbeat", back_populates="asset")

    # Relationship to PortFinding (one-to-many)
    port_findings = relationship("PortFinding", back_populates="asset")
    
    def __repr__(self) -> str:
        return f"<Asset(id={self.id}, hostname={self.hostname}, asset_type={self.asset_type}, status={self.status})>"
