"""Event model for security event ingestion."""

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.user import Base


class Event(Base):
    """Security event model for raw event ingestion.

    Stores security events ingested from agents or analysts.
    Linked to Asset model via asset_id foreign key (optional).
    """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    source_ip = Column(String(45), nullable=True, index=True)  # IPv6 max length = 45
    event_type = Column(String(30), nullable=False, index=True)
    severity = Column(String(10), nullable=False, index=True)
    raw_data = Column(JSON, nullable=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relations
    correlation_groups = relationship(
        "CorrelationGroup",
        secondary="correlation_events",
        back_populates="events"
    )

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, event_type={self.event_type}, severity={self.severity})>"
