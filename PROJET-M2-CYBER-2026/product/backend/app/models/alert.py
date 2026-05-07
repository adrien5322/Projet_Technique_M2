"""Alert model for security alert management."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.user import Base


class Alert(Base):
    """Alert model representing security alerts detected by the SOC."""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String(2000), nullable=False)
    severity = Column(SAEnum("low", "medium", "high", "critical", name="severity_enum"), nullable=False, default="low", index=True)
    status = Column(SAEnum("new", "investigating", "resolved", "false_positive", name="status_enum"), nullable=False, default="new", index=True)
    source_event_id = Column(String(255), nullable=True, index=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship to User (assigned analyst)
    assignee = relationship("User", foreign_keys=[assigned_to])

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, title={self.title}, severity={self.severity}, status={self.status})>"
