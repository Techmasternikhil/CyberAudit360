from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import json
from datetime import datetime, timezone

from app.dependencies import get_db
import app.models as models
import app.schemas as schemas
from app.services.inventory_service import InventoryService
from app.scanners.port_scanner import PortScanner
from app.services.risk_engine import RiskEngine
from app.services.evidence_service import EvidenceService
from app.services.framework_mapper import FrameworkMapper
from app.services.reporting_service import ReportingService
from app.services.seed_service import SeedService

router = APIRouter()

# --- Aggregated Dashboard Summary ---
@router.get("/dashboard")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """High-performance consolidated dashboard endpoint returning findings, assets, score, and compliance coverage."""
    findings = db.query(models.finding.Finding).all()
    assets = db.query(models.asset.Asset).all()
    score_data = RiskEngine.calculate_overall_security_score(findings)
    coverage = FrameworkMapper.calculate_coverage(findings)
    
    return {
        "findings": findings,
        "assets": assets,
        "score": score_data["score"],
        "score_explanation": score_data.get("explanation"),
        "coverage": coverage
    }

# --- Assets ---
@router.get("/assets", response_model=List[schemas.Asset])
def get_assets(db: Session = Depends(get_db)):
    return db.query(models.asset.Asset).all()

@router.post("/assets", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    asset_data = asset.model_dump()
    if not asset_data.get("id"):
        asset_data["id"] = str(uuid.uuid4())
    db_asset = models.asset.Asset(**asset_data)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# --- Findings ---
@router.get("/findings", response_model=List[schemas.Finding])
def get_findings(db: Session = Depends(get_db)):
    return db.query(models.finding.Finding).all()

@router.get("/findings/{finding_id}", response_model=schemas.Finding)
def get_finding(finding_id: str, db: Session = Depends(get_db)):
    finding = db.query(models.finding.Finding).filter(models.finding.Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding

@router.post("/findings", response_model=schemas.Finding)
def create_finding(finding_in: schemas.FindingCreate, db: Session = Depends(get_db)):
    finding_data = finding_in.model_dump()
    if not finding_data.get("id"):
        finding_data["id"] = str(uuid.uuid4())
    
    # Check if asset exists
    asset = db.query(models.asset.Asset).filter(models.asset.Asset.id == finding_data["asset_id"]).first()
    
    db_finding = models.finding.Finding(**finding_data)
    # Calculate risk score
    db_finding.risk_score = RiskEngine.calculate_finding_risk(db_finding, asset_criticality=asset)
    
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    return db_finding

@router.patch("/findings/{finding_id}", response_model=schemas.Finding)
def update_finding(finding_id: str, finding_update: schemas.FindingUpdate, db: Session = Depends(get_db)):
    finding = db.query(models.finding.Finding).filter(models.finding.Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    update_dict = finding_update.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        setattr(finding, field, val)
    
    # Recalculate risk if severity, likelihood, or impact changed
    asset = db.query(models.asset.Asset).filter(models.asset.Asset.id == finding.asset_id).first()
    finding.risk_score = RiskEngine.calculate_finding_risk(finding, asset_criticality=asset)
    
    db.commit()
    db.refresh(finding)
    return finding

@router.patch("/findings/{finding_id}/toggle-status")
def toggle_finding_status(finding_id: str, db: Session = Depends(get_db)):
    finding = db.query(models.finding.Finding).filter(models.finding.Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    if finding.status == models.finding.FindingStatus.OPEN:
        finding.status = models.finding.FindingStatus.RESOLVED
    else:
        finding.status = models.finding.FindingStatus.OPEN
        
    db.commit()
    db.refresh(finding)
    return {"status": "success", "id": finding.id, "new_status": finding.status}

@router.delete("/findings/{finding_id}")
def delete_finding(finding_id: str, db: Session = Depends(get_db)):
    finding = db.query(models.finding.Finding).filter(models.finding.Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    db.delete(finding)
    db.commit()
    return {"status": "success", "message": f"Finding {finding_id} deleted"}

# --- Security Score & Risk ---
@router.get("/score")
def get_security_score(db: Session = Depends(get_db)):
    findings = db.query(models.finding.Finding).all()
    return RiskEngine.calculate_overall_security_score(findings)

# --- Compliance Framework Mapping ---
@router.get("/compliance/coverage")
def get_compliance_coverage(db: Session = Depends(get_db)):
    findings = db.query(models.finding.Finding).all()
    coverage = FrameworkMapper.calculate_coverage(findings)
    
    # Also provide framework mapping breakdown for each finding
    mapped_findings = []
    for f in findings:
        mapped_findings.append({
            "id": f.id,
            "title": f.title,
            "severity": f.severity.value if hasattr(f.severity, "value") else str(f.severity),
            "status": f.status.value if hasattr(f.status, "value") else str(f.status),
            "mappings": FrameworkMapper.map_finding(f.title, f.description or "")
        })
    
    return {
        "coverage": coverage,
        "frameworks": FrameworkMapper.SUPPORTED_FRAMEWORKS,
        "mapped_findings": mapped_findings
    }

# --- Evidence Tracking ---
@router.get("/evidence", response_model=List[schemas.Evidence])
def get_evidence_records(db: Session = Depends(get_db)):
    return db.query(models.evidence.Evidence).all()

@router.post("/evidence", response_model=schemas.Evidence)
def create_evidence_record(evidence_in: schemas.EvidenceCreate, db: Session = Depends(get_db)):
    db_evidence = EvidenceService.create_evidence_model(
        evidence_type=evidence_in.evidence_type,
        source=evidence_in.source,
        collector=evidence_in.collector,
        description=evidence_in.description,
        hash_value=evidence_in.hash_value,
        related_control=evidence_in.related_control,
        id=evidence_in.id
    )
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence

# --- Remediation Workflow ---
@router.get("/remediations", response_model=List[schemas.Remediation])
def get_remediations(db: Session = Depends(get_db)):
    return db.query(models.remediation.Remediation).all()

@router.get("/findings/{finding_id}/remediation", response_model=Optional[schemas.Remediation])
def get_finding_remediation(finding_id: str, db: Session = Depends(get_db)):
    remediation = db.query(models.remediation.Remediation).filter(
        models.remediation.Remediation.finding_id == finding_id
    ).first()
    return remediation

@router.post("/findings/{finding_id}/remediation", response_model=schemas.Remediation)
def create_or_update_remediation(finding_id: str, rem_in: schemas.RemediationCreate, db: Session = Depends(get_db)):
    finding = db.query(models.finding.Finding).filter(models.finding.Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    existing = db.query(models.remediation.Remediation).filter(
        models.remediation.Remediation.finding_id == finding_id
    ).first()
    
    rem_data = rem_in.model_dump()
    rem_data["finding_id"] = finding_id
    
    if existing:
        for k, v in rem_data.items():
            if k != "id" and v is not None:
                setattr(existing, k, v)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        if not rem_data.get("id"):
            rem_data["id"] = str(uuid.uuid4())
        new_rem = models.remediation.Remediation(**rem_data)
        db.add(new_rem)
        db.commit()
        db.refresh(new_rem)
        return new_rem

# --- Live Scan with Evidence Hashing ---
@router.post("/scan")
def trigger_live_scan(db: Session = Depends(get_db)):
    # 1. Run local inventory and get/update asset
    asset = InventoryService.discover_local_asset(db)
    
    # 2. Run port scan on localhost using unified default ports
    open_ports = PortScanner.scan_target("127.0.0.1", ports=PortScanner.get_default_ports())
    
    # 3. Create cryptographically hashed evidence of the scan output
    scan_payload_bytes = json.dumps({
        "target": "127.0.0.1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "open_ports": open_ports,
        "asset_hostname": asset.hostname
    }, sort_keys=True).encode("utf-8")
    
    scan_evidence = EvidenceService.create_evidence_model(
        evidence_type="SCAN_RESULT",
        source="Localhost Network Socket (127.0.0.1)",
        collector="PortScanner Engine v1.0",
        description=f"Local port scan executed against 127.0.0.1 identifying {len(open_ports)} listening socket services.",
        content=scan_payload_bytes,
        related_control="CIS 4.1 / NIST PR.IP-01"
    )
    db.add(scan_evidence)
    db.commit()
    
    # 4. Create findings for open ports linked to this evidence
    created_findings = []
    for p in open_ports:
        port_num = p["port"]
        service_name = p.get("service", "Unknown")
        # Avoid duplicate findings for the same port on the same asset
        existing = db.query(models.finding.Finding).filter(
            models.finding.Finding.asset_id == asset.id,
            models.finding.Finding.title == f"Open Port: {port_num}"
        ).first()
        
        if not existing:
            finding_id = str(uuid.uuid4())
            sev_name = PortScanner.get_port_severity(port_num)
            severity = getattr(models.finding.Severity, sev_name, models.finding.Severity.INFORMATIONAL)
            
            finding = models.finding.Finding(
                id=finding_id,
                asset_id=asset.id,
                evidence_id=scan_evidence.id,
                title=f"Open Port: {port_num}",
                description=f"Port {port_num} ({service_name}) was detected actively listening on local interface.",
                category="Network Exposure",
                severity=severity,
                likelihood=2,
                impact=2,
                status=models.finding.FindingStatus.OPEN,
                is_demo=False
            )
            finding.risk_score = RiskEngine.calculate_finding_risk(finding, asset_criticality=asset)
            
            db.add(finding)
            created_findings.append(finding)
    
    if created_findings:
        db.commit()
        
    return {
        "status": "success",
        "asset": asset.hostname,
        "new_findings_count": len(created_findings),
        "total_open_ports": len(open_ports),
        "evidence_id": scan_evidence.id,
        "evidence_hash": scan_evidence.hash_value
    }

# --- Enterprise Demo Scenarios ---
@router.post("/demo/seed")
def seed_demo(db: Session = Depends(get_db)):
    SeedService.seed_demo_scenario(db)
    return {"status": "success", "message": "Enterprise demo scenario loaded successfully"}

@router.post("/demo/reset")
def reset_demo(db: Session = Depends(get_db)):
    SeedService.reset_all_data(db)
    return {"status": "success", "message": "All findings and assets reset to clean state"}

# --- Executive Reporting Export ---
@router.get("/report/export")
def export_audit_report(format: str = "docx", db: Session = Depends(get_db)):
    audit = db.query(models.audit.Audit).first()
    findings = db.query(models.finding.Finding).all()
    
    if format.lower() == "md":
        report_text = ReportingService.get_report_text(audit, findings)
        return Response(
            content=report_text,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=CyberAudit360_Report.md"}
        )
    
    # Default to professional Word document (.docx)
    docx_stream = ReportingService.generate_docx_stream(audit, findings)
    return Response(
        content=docx_stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=CyberAudit360_Executive_Report.docx"}
    )
