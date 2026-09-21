from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database import Base

class AuditStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FOLLOW_UP = "FOLLOW_UP"

class Audit(Base):
    __tablename__ = "audits"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    auditor = Column(String)
    organization = Column(String)
    scope = Column(String)
    assessment_type = Column(String)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    status = Column(Enum(AuditStatus), default=AuditStatus.PLANNED)
    notes = Column(String, nullable=True)

    findings = relationship("Finding", back_populates="audit")
