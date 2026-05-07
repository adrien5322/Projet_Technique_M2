"""Correlation models for grouping related security events."""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.user import Base


# Table d'association pour la relation many-to-many entre CorrelationGroup et Event
correlation_events = Table(
    "correlation_events",
    Base.metadata,
    Column("correlation_id", Integer, ForeignKey("correlation_groups.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
)


class CorrelationGroup(Base):
    """Correlation group model for grouping related security events.
    
    Groups events based on correlation rules like:
    - IP source matching
    - Temporal proximity
    - Other correlation criteria
    """
    
    __tablename__ = "correlation_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_type = Column(String(50), nullable=False, index=True)  # "ip_source", "temporal"
    rule_key = Column(String(255), nullable=False, index=True)  # IP address ou clé de corrélation
    severity = Column(String(20), nullable=False, default="medium", index=True)  # "low", "medium", "high", "critical"
    score = Column(Integer, nullable=False, default=0)  # Score de corrélation (0-100)
    event_count = Column(Integer, nullable=False, default=0)
    first_seen = Column(DateTime, nullable=False)
    last_seen = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), nullable=False, default="open", index=True)  # "open", "investigating", "resolved", "false_positive"
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relations
    events = relationship("Event", secondary=correlation_events, back_populates="correlation_groups")
    assignee = relationship("User")
    
    def __repr__(self) -> str:
        return f"<CorrelationGroup(id={self.id}, rule_type={self.rule_type}, rule_key={self.rule_key})>"
