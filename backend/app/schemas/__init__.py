
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
    id: Optional[str] = None

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
    id: Optional[str] = None
    asset_id: str
    audit_id: Optional[str] = None

class FindingUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[Severity] = None
    likelihood: Optional[int] = None
    impact: Optional[int] = None
    cvss_score: Optional[float] = None
    cvss_vector: Optional[str] = None
    cve: Optional[str] = None
    cwe: Optional[str] = None
    kev_status: Optional[bool] = None
    internet_exposed: Optional[bool] = None
    recommendation: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[FindingStatus] = None

class Finding(FindingBase):
    id: str
    asset_id: str
    audit_id: Optional[str] = None
    evidence_id: Optional[str] = None
    risk_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

class EvidenceBase(BaseSchema):
    evidence_type: EvidenceType = EvidenceType.SCAN_RESULT
    source: str
    collector: str
    description: str
    hash_value: Optional[str] = None
    related_control: Optional[str] = None
    integrity_status: str = "VERIFIED"

class EvidenceCreate(EvidenceBase):
    id: Optional[str] = None

class Evidence(EvidenceBase):
    id: str
    timestamp: datetime

class RemediationBase(BaseSchema):
    finding_id: str
    owner: str
    action: str
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None
    status: RemediationStatus = RemediationStatus.OPEN
    notes: Optional[str] = None
    verification_method: Optional[str] = None

class RemediationCreate(RemediationBase):
    id: Optional[str] = None

class Remediation(RemediationBase):
    id: str
    verification_date: Optional[datetime] = None
    verified_by: Optional[str] = None

