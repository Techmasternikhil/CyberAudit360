from sqlalchemy import Column, String, Enum, DateTime
import enum
from datetime import datetime, timezone
from app.database import Base

class ControlStatus(str, enum.Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class Control(Base):
    __tablename__ = "controls"
    
    id = Column(String, primary_key=True, index=True)
    framework = Column(String) # e.g. NIST CSF 2.0, CIS Controls v8.1
    control_id = Column(String) # e.g. PR.AC-1
    title = Column(String)
    status = Column(Enum(ControlStatus), default=ControlStatus.NOT_APPLICABLE)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    evidence = Column(String, nullable=True)
    explanation = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)
