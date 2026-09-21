
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.asset import AssetType, BusinessCriticality
from app.models.audit import AuditStatus
from app.models.finding import Severity, FindingStatus
from app.models.evidence import EvidenceType
from app.models.remediation import RemediationStatus
from app.models.control import ControlStatus

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AssetBase(BaseSchema):
    hostname: str
    ip_address: str
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    architecture: Optional[str] = None
    asset_type: AssetType = AssetType.UNKNOWN
    owner: Optional[str] = None
    business_criticality: BusinessCriticality = BusinessCriticality.LOW
    environment: Optional[str] = None
    notes: Optional[str] = None
    discovery_source: str
    status: str = "ACTIVE"

class AssetCreate(AssetBase):
    id: str

class Asset(AssetBase):
    id: str
    discovery_timestamp: datetime

class FindingBase(BaseSchema):
    title: str
    description: str
    category: str
    severity: Severity
    likelihood: int = 3
    impact: int = 3
    cvss_score: Optional[float] = None
    cvss_vector: Optional[str] = None
    cve: Optional[str] = None
    cwe: Optional[str] = None
    kev_status: bool = False
    internet_exposed: bool = False
    recommendation: Optional[str] = None
    owner: Optional[str] = None
    status: FindingStatus = FindingStatus.OPEN
    is_demo: bool = False

class FindingCreate(FindingBase):
    id: str
    asset_id: str
    audit_id: Optional[str] = None

class Finding(FindingBase):
    id: str
    asset_id: str
    audit_id: Optional[str] = None
    evidence_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

