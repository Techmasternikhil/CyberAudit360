import os

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

schemas_base = """
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

"""

create_file("e:/Projects/CyberAudit360/backend/app/schemas/__init__.py", schemas_base)

api_base = """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.dependencies import get_db
import app.models as models
import app.schemas as schemas
import uuid
from datetime import datetime

router = APIRouter()

@router.get("/assets", response_model=List[schemas.Asset])
def get_assets(db: Session = Depends(get_db)):
    return db.query(models.asset.Asset).all()

@router.post("/assets", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    db_asset = models.asset.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/findings", response_model=List[schemas.Finding])
def get_findings(db: Session = Depends(get_db)):
    return db.query(models.finding.Finding).all()
"""

create_file("e:/Projects/CyberAudit360/backend/app/api/router.py", api_base)

main_py_update = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.router import router as api_router
from app.models import init_db

init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/api/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

app.include_router(api_router, prefix="/api")
"""
create_file("e:/Projects/CyberAudit360/backend/app/main.py", main_py_update)

print("Backend base setup generated successfully.")
