from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database import Base

class RemediationStatus(str, enum.Enum):
    OPEN = "OPEN"
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    READY_FOR_VERIFICATION = "READY_FOR_VERIFICATION"
    VERIFIED = "VERIFIED"
    CLOSED = "CLOSED"

class Remediation(Base):
    __tablename__ = "remediations"
    
    id = Column(String, primary_key=True, index=True)
    finding_id = Column(String, ForeignKey("findings.id"))
    
    owner = Column(String)
    action = Column(String)
    priority = Column(String)
    due_date = Column(DateTime, nullable=True)
    status = Column(Enum(RemediationStatus), default=RemediationStatus.OPEN)
    notes = Column(String, nullable=True)
    
    verification_method = Column(String, nullable=True)
    verification_date = Column(DateTime, nullable=True)
    verified_by = Column(String, nullable=True)

    finding = relationship("Finding", back_populates="remediation")
