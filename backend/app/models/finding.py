from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database import Base

class Severity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"

class FindingStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    MITIGATED = "MITIGATED"
    RESOLVED = "RESOLVED"
    RISK_ACCEPTED = "RISK_ACCEPTED"
    FALSE_POSITIVE = "FALSE_POSITIVE"

class Finding(Base):
    __tablename__ = "findings"
    
    id = Column(String, primary_key=True, index=True)
    audit_id = Column(String, ForeignKey("audits.id"), nullable=True)
    asset_id = Column(String, ForeignKey("assets.id"))
    
    title = Column(String)
    description = Column(String)
    category = Column(String)
    severity = Column(Enum(Severity))
    likelihood = Column(Integer, default=3)
    impact = Column(Integer, default=3)
    risk_score = Column(Float, nullable=True)
    
    cvss_score = Column(Float, nullable=True)
    cvss_vector = Column(String, nullable=True)
    cve = Column(String, nullable=True)
    cwe = Column(String, nullable=True)
    kev_status = Column(Boolean, default=False)
    internet_exposed = Column(Boolean, default=False)
    
    evidence_id = Column(String, ForeignKey("evidence.id"), nullable=True)
    recommendation = Column(String, nullable=True)
    remediation_deadline = Column(DateTime, nullable=True)
    owner = Column(String, nullable=True)
    
    status = Column(Enum(FindingStatus), default=FindingStatus.OPEN)
    is_demo = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    asset = relationship("Asset", back_populates="findings")
    audit = relationship("Audit", back_populates="findings")
    evidence = relationship("Evidence", back_populates="finding")
    remediation = relationship("Remediation", back_populates="finding", uselist=False)
