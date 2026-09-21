import os
import sys
import uuid
from datetime import datetime, timedelta

# Add backend directory to sys path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, engine
from app.models import init_db
from app.models.asset import Asset, AssetType, BusinessCriticality
from app.models.finding import Finding, Severity, FindingStatus
from app.models.audit import Audit, AuditStatus

def seed_demo_data():
    init_db()
    db = SessionLocal()
    
    print("Clearing existing data for DEMO...")
    db.query(Finding).delete()
    db.query(Asset).delete()
    db.query(Audit).delete()
    db.commit()
    
    print("Seeding Audit...")
    audit = Audit(
        id=str(uuid.uuid4()),
        name="Q3 Enterprise Security Assessment",
        auditor="NexusBridge SOC Team",
        organization="NexusBridge Technologies Pvt. Ltd.",
        scope="Internal Network & Cloud Resources",
        assessment_type="Comprehensive DEMO",
        status=AuditStatus.IN_PROGRESS
    )
    db.add(audit)
    
    print("Seeding Assets...")
    assets = [
        Asset(id=str(uuid.uuid4()), hostname="DC-01.nexusbridge.local", ip_address="10.0.0.10", os_name="Windows Server", os_version="2022", asset_type=AssetType.SERVER, business_criticality=BusinessCriticality.CRITICAL, discovery_source="DEMO"),
        Asset(id=str(uuid.uuid4()), hostname="WEB-FRONT-01", ip_address="192.168.1.100", os_name="Linux", os_version="Ubuntu 22.04", asset_type=AssetType.SERVER, business_criticality=BusinessCriticality.HIGH, discovery_source="DEMO"),
        Asset(id=str(uuid.uuid4()), hostname="VPN-GW-01", ip_address="203.0.113.10", os_name="pfSense", os_version="2.6.0", asset_type=AssetType.NETWORK_DEVICE, business_criticality=BusinessCriticality.CRITICAL, discovery_source="DEMO")
    ]
    db.add_all(assets)
    db.commit()
    
    print("Seeding Demo Findings...")
    findings = [
        Finding(
            id="V-001",
            audit_id=audit.id,
            asset_id=assets[2].id,
            title="Internet-Facing Remote Access Vulnerability",
            description="DEMO DATA: VPN gateway is running an outdated firmware version with a known RCE vulnerability.",
            category="Network Security",
            severity=Severity.CRITICAL,
            likelihood=4, impact=5,
            cvss_score=9.8,
            kev_status=True,
            internet_exposed=True,
            recommendation="Patch the VPN gateway immediately and restrict admin interfaces.",
            status=FindingStatus.OPEN,
            is_demo=True
        ),
        Finding(
            id="V-002",
            audit_id=audit.id,
            asset_id=assets[1].id,
            title="Outdated web framework dependency",
            description="DEMO DATA: Web server uses an old version of Log4j which is vulnerable to remote code execution.",
            category="Application Security",
            severity=Severity.HIGH,
            likelihood=4, impact=4,
            cvss_score=8.1,
            internet_exposed=True,
            recommendation="Update Log4j to version 2.17.1 or higher.",
            status=FindingStatus.IN_PROGRESS,
            is_demo=True
        ),
        Finding(
            id="V-003",
            audit_id=audit.id,
            asset_id=assets[0].id,
            title="Excessive privileged account permissions",
            description="DEMO DATA: Several service accounts have Domain Admin privileges unnecessarily.",
            category="Identity & Access",
            severity=Severity.HIGH,
            likelihood=3, impact=4,
            cvss_score=7.2,
            internet_exposed=False,
            recommendation="Implement Principle of Least Privilege for service accounts.",
            status=FindingStatus.OPEN,
            is_demo=True
        )
    ]
    db.add_all(findings)
    db.commit()
    
    print("Demo Data Seeded Successfully!")
    db.close()

if __name__ == "__main__":
    seed_demo_data()
