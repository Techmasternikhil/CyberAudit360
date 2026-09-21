import uuid
from sqlalchemy.orm import Session
from app.models.asset import Asset, AssetType, BusinessCriticality
from app.models.finding import Finding, Severity, FindingStatus
from app.models.audit import Audit, AuditStatus
from app.models.evidence import Evidence
from app.models.remediation import Remediation
from app.services.risk_engine import RiskEngine

class SeedService:
    @staticmethod
    def seed_demo_scenario(db: Session):
        """Seeds the enterprise demo scenario (NexusBridge Technologies)."""
        # Ensure an audit exists
        audit = db.query(Audit).filter(Audit.name == "Q3 Enterprise Security Assessment").first()
        if not audit:
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
            db.commit()
            db.refresh(audit)

        # Assets
        assets = [
            Asset(id="demo-asset-1", hostname="DC-01.nexusbridge.local", ip_address="10.0.0.10", os_name="Windows Server", os_version="2022", asset_type=AssetType.SERVER, business_criticality=BusinessCriticality.CRITICAL, discovery_source="DEMO"),
            Asset(id="demo-asset-2", hostname="WEB-FRONT-01", ip_address="192.168.1.100", os_name="Linux", os_version="Ubuntu 22.04", asset_type=AssetType.SERVER, business_criticality=BusinessCriticality.HIGH, discovery_source="DEMO"),
            Asset(id="demo-asset-3", hostname="VPN-GW-01", ip_address="203.0.113.10", os_name="pfSense", os_version="2.6.0", asset_type=AssetType.NETWORK_DEVICE, business_criticality=BusinessCriticality.CRITICAL, discovery_source="DEMO")
        ]

        for a in assets:
            if not db.query(Asset).filter(Asset.id == a.id).first():
                db.add(a)
        db.commit()

        # Findings
        demo_findings = [
            {
                "id": "DEMO-001",
                "asset_id": "demo-asset-3",
                "title": "Internet-Facing Remote Access Vulnerability",
                "description": "DEMO DATA: VPN gateway is running an outdated firmware version with a known RCE vulnerability.",
                "category": "Network Security",
                "severity": Severity.CRITICAL,
                "likelihood": 4, "impact": 5, "cvss_score": 9.8, "kev_status": True, "internet_exposed": True,
                "recommendation": "Patch the VPN gateway immediately and restrict admin interfaces."
            },
            {
                "id": "DEMO-002",
                "asset_id": "demo-asset-2",
                "title": "Outdated web framework dependency",
                "description": "DEMO DATA: Web server uses an old version of Log4j which is vulnerable to remote code execution.",
                "category": "Application Security",
                "severity": Severity.HIGH,
                "likelihood": 4, "impact": 4, "cvss_score": 8.1, "kev_status": False, "internet_exposed": True,
                "recommendation": "Update Log4j to version 2.17.1 or higher."
            },
            {
                "id": "DEMO-003",
                "asset_id": "demo-asset-1",
                "title": "Excessive privileged account permissions",
                "description": "DEMO DATA: Several service accounts have Domain Admin privileges unnecessarily.",
                "category": "Identity & Access",
                "severity": Severity.HIGH,
                "likelihood": 3, "impact": 4, "cvss_score": 7.2, "kev_status": False, "internet_exposed": False,
                "recommendation": "Implement Principle of Least Privilege for service accounts."
            }
        ]

        for item in demo_findings:
            if not db.query(Finding).filter(Finding.id == item["id"]).first():
                f = Finding(
                    id=item["id"],
                    audit_id=audit.id,
                    asset_id=item["asset_id"],
                    title=item["title"],
                    description=item["description"],
                    category=item["category"],
                    severity=item["severity"],
                    likelihood=item["likelihood"],
                    impact=item["impact"],
                    cvss_score=item["cvss_score"],
                    kev_status=item["kev_status"],
                    internet_exposed=item["internet_exposed"],
                    recommendation=item["recommendation"],
                    status=FindingStatus.OPEN,
                    is_demo=True
                )
                f.risk_score = RiskEngine.calculate_finding_risk(f, asset_criticality="CRITICAL")
                db.add(f)
        db.commit()

    @staticmethod
    def reset_all_data(db: Session):
        """Clears all remediations, findings, evidence, assets, and audits for a fresh clean state."""
        db.query(Remediation).delete()
        db.query(Finding).delete()
        db.query(Evidence).delete()
        db.query(Asset).delete()
        db.query(Audit).delete()
        db.commit()
