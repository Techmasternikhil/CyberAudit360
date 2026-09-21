from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database import Base

class AssetType(str, enum.Enum):
    SERVER = "SERVER"
    WORKSTATION = "WORKSTATION"
    NETWORK_DEVICE = "NETWORK_DEVICE"
    DATABASE = "DATABASE"
    CLOUD_RESOURCE = "CLOUD_RESOURCE"
    UNKNOWN = "UNKNOWN"

class BusinessCriticality(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(String, primary_key=True, index=True)
    hostname = Column(String, index=True)
    ip_address = Column(String, index=True)
    os_name = Column(String)
    os_version = Column(String)
    architecture = Column(String)
    asset_type = Column(Enum(AssetType), default=AssetType.UNKNOWN)
    owner = Column(String, nullable=True)
    business_criticality = Column(Enum(BusinessCriticality), default=BusinessCriticality.LOW)
    environment = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    discovery_source = Column(String)
    discovery_timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="ACTIVE")

    # Relationships
    findings = relationship("Finding", back_populates="asset")
