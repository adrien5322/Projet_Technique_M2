"""Telemetry models for heartbeat monitoring."""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.user import Base


class TelemetryHeartbeat(Base):
    """Telemetry heartbeat model for asset monitoring.
    
    Tracks asset status including CPU, memory, disk usage and network latency.
    Linked to Asset model via asset_id foreign key.
    """
    
    __tablename__ = "telemetry_heartbeats"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="online")
    cpu_usage = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    disk_usage = Column(Float, nullable=True)
    network_latency = Column(Float, nullable=True)
    
    # Relationship to Asset
    asset = relationship("Asset", back_populates="heartbeats")
    
    def __repr__(self) -> str:
        return f"<TelemetryHeartbeat(asset_id={self.asset_id}, status={self.status}, timestamp={self.timestamp})>"
