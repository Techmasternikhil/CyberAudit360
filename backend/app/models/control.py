from sqlalchemy import Column, String, Enum, DateTime
import enum
from datetime import datetime
from app.database import Base

class ControlStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    NOT_ASSESSED = "NOT_ASSESSED"

class Control(Base):
    __tablename__ = "controls"
    
    id = Column(String, primary_key=True, index=True)
    control_id = Column(String, index=True)
    status = Column(Enum(ControlStatus), default=ControlStatus.NOT_ASSESSED)
    severity = Column(String, nullable=True)
    evidence = Column(String, nullable=True)
    explanation = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
