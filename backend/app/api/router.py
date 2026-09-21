
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.dependencies import get_db
import app.models as models
import app.schemas as schemas
import uuid
from datetime import datetime
from app.services.inventory_service import InventoryService
from app.scanners.port_scanner import PortScanner
from app.services.risk_engine import RiskEngine

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

@router.get("/score")
def get_security_score(db: Session = Depends(get_db)):
    findings = db.query(models.finding.Finding).all()
    return RiskEngine.calculate_overall_security_score(findings)

@router.post("/scan")
def trigger_live_scan(db: Session = Depends(get_db)):
    # 1. Run local inventory and get/update asset
    asset = InventoryService.discover_local_asset(db)
    
    # 2. Run port scan on localhost (including frontend and backend dev ports)
    ports_to_check = [21, 22, 23, 25, 53, 80, 135, 139, 443, 445, 1433, 3306, 3389, 5173, 5432, 8000, 8080]
    open_ports = PortScanner.scan_target("127.0.0.1", ports=ports_to_check)
    
    # 3. Create findings for open ports
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
            severity = models.finding.Severity.INFORMATIONAL
            if port_num in [21, 23]: # Telnet/FTP
                severity = models.finding.Severity.HIGH
            elif port_num in [22, 3389, 445]: # SSH, RDP, SMB
                severity = models.finding.Severity.MEDIUM
            elif port_num in [5173, 8000, 8080, 80]:
                severity = models.finding.Severity.LOW
            
            finding = models.finding.Finding(
                id=finding_id,
                asset_id=asset.id,
                title=f"Open Port: {port_num}",
                description=f"Port {port_num} ({service_name}) was detected actively listening on local interface.",
                category="Network Exposure",
                severity=severity,
                likelihood=2,
                impact=2,
                status=models.finding.FindingStatus.OPEN,
                is_demo=False
            )
            
            crit_str = asset.business_criticality.value if hasattr(asset.business_criticality, "value") else str(asset.business_criticality or "MEDIUM")
            finding.risk_score = RiskEngine.calculate_finding_risk(finding, asset_criticality=crit_str)
            
            db.add(finding)
            created_findings.append(finding)
    
    if created_findings:
        db.commit()
        
    return {
        "status": "success",
        "asset": asset.hostname,
        "new_findings_count": len(created_findings),
        "total_open_ports": len(open_ports)
    }

@router.post("/demo/seed")
def seed_demo(db: Session = Depends(get_db)):
    from app.services.seed_service import SeedService
    SeedService.seed_demo_scenario(db)
    return {"status": "success", "message": "Enterprise demo scenario loaded successfully"}

@router.post("/demo/reset")
def reset_demo(db: Session = Depends(get_db)):
    from app.services.seed_service import SeedService
    SeedService.reset_all_data(db)
    return {"status": "success", "message": "All findings and assets reset to clean state"}

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

@router.get("/report/export")
def export_audit_report(format: str = "docx", db: Session = Depends(get_db)):
    from fastapi.responses import Response
    from app.services.reporting_service import ReportingService
    
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
