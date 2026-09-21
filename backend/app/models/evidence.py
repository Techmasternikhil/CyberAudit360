from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timezone
from app.database import Base

class EvidenceType(str, enum.Enum):
    SYSTEM_OUTPUT = "SYSTEM_OUTPUT"
    CONFIGURATION = "CONFIGURATION"
    LOG = "LOG"
    SCREENSHOT = "SCREENSHOT"
    SCAN_RESULT = "SCAN_RESULT"
    DOCUMENT = "DOCUMENT"
    INTERVIEW = "INTERVIEW"
    MANUAL_OBSERVATION = "MANUAL_OBSERVATION"

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, index=True)
    evidence_type = Column(Enum(EvidenceType))
    source = Column(String)
    collector = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    description = Column(String)
    hash_value = Column(String, nullable=True) # SHA-256
    
    related_control = Column(String, nullable=True)
    integrity_status = Column(String, default="VERIFIED")
    
    finding = relationship("Finding", back_populates="evidence", uselist=False)
