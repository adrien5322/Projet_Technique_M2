"""PortFinding model for network discovery results."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.user import Base


class PortFinding(Base):
    """Model representing a discovered port on an asset.

    Created during network port scanning to track open/closed/filtered
    ports and associated service information.
    """

    __tablename__ = "port_findings"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    port = Column(Integer, nullable=False)
    protocol = Column(String(10), nullable=False, default="tcp")
    service_name = Column(String(100), nullable=False)
    service_version = Column(String(200), nullable=True)
    state = Column(String(20), nullable=False, default="open")
    discovered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship back to Asset
    asset = relationship("Asset", back_populates="port_findings")

    def __repr__(self) -> str:
        return (
            f"<PortFinding(id={self.id}, asset_id={self.asset_id}, "
            f"port={self.port}/{self.protocol}, service={self.service_name}, "
            f"state={self.state})>"
        )
