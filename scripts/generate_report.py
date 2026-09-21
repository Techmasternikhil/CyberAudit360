import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal
from app.models.audit import Audit
from app.models.finding import Finding
from app.services.reporting_service import ReportingService

def generate_sample_report():
    db = SessionLocal()
    audit = db.query(Audit).first()
    findings = db.query(Finding).all()
    
    if audit and findings:
        report_path = ReportingService.generate_markdown_report(audit, findings, output_dir="../reports")
        print(f"Report successfully generated at: {report_path}")
    else:
        print("Could not find audit or findings in database.")
    db.close()

if __name__ == "__main__":
    generate_sample_report()
