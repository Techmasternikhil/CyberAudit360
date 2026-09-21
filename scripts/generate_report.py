import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

sys.path.append(BACKEND_DIR)

from app.database import SessionLocal
from app.models.audit import Audit
from app.models.finding import Finding
from app.services.reporting_service import ReportingService

def generate_sample_reports():
    """Generates official audit reports in both Markdown and Microsoft Word (.docx) formats."""
    db = SessionLocal()
    try:
        audit = db.query(Audit).first()
        findings = db.query(Finding).all()
        
        if audit and findings:
            md_path = ReportingService.generate_markdown_report(audit, findings, output_dir=REPORTS_DIR)
            docx_path = ReportingService.generate_docx_report(audit, findings, output_dir=REPORTS_DIR)
            print(f"[+] Audit reports generated successfully:")
            print(f"    - Markdown:    {md_path}")
            print(f"    - Word (.docx): {docx_path}")
        else:
            print("[!] No audit or findings found in database. Please run or seed a scan first.")
    finally:
        db.close()

if __name__ == "__main__":
    generate_sample_reports()
