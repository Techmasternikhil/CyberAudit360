import pytest
import io
import docx
from app.services.reporting_service import ReportingService
from app.models.audit import Audit
from app.models.finding import Finding, Severity, FindingStatus

@pytest.fixture
def sample_audit():
    return Audit(
        id="audit-test-01",
        name="Production Readiness Security Assessment",
        organization="Acme Enterprise Corp",
        auditor="Lead Cyber Auditor",
        scope="Local Workstation & Network Services"
    )

@pytest.fixture
def sample_findings():
    return [
        Finding(
            id="f-01",
            title="Firewall Disabled",
            description="Local host firewall is turned off.",
            severity=Severity.HIGH,
            status=FindingStatus.OPEN,
            category="Network Exposure",
            cvss_score=7.5,
            recommendation="Enable Windows Defender or iptables firewall immediately."
        ),
        Finding(
            id="f-02",
            title="Open Port: 3389",
            description="Port 3389 (RDP) listening on network interface.",
            severity=Severity.MEDIUM,
            status=FindingStatus.RESOLVED,
            category="Remote Access",
            cvss_score=5.5,
            recommendation="Restrict RDP access via VPN and MFA."
        )
    ]

def test_markdown_report_generation(sample_audit, sample_findings):
    md_report = ReportingService.get_report_text(sample_audit, sample_findings)
    assert "# Cybersecurity Audit Report:" in md_report
    assert "Acme Enterprise Corp" in md_report
    assert "Lead Cyber Auditor" in md_report
    assert "Firewall Disabled" in md_report
    assert "Open Port: 3389" in md_report
    assert "Executive Summary" in md_report
    assert "Framework Coverage" in md_report

def test_docx_stream_generation(sample_audit, sample_findings):
    stream = ReportingService.generate_docx_stream(sample_audit, sample_findings)
    assert isinstance(stream, io.BytesIO)
    stream_bytes = stream.getvalue()
    
    # Check that stream is non-empty and has DOCX zip header magic bytes (PK\x03\x04)
    assert len(stream_bytes) > 1000
    assert stream_bytes[:4] == b"PK\x03\x04"
    
    # Verify it can be loaded by python-docx without error
    stream.seek(0)
    doc = docx.Document(stream)
    text_content = "\n".join([p.text for p in doc.paragraphs])
    assert "EXECUTIVE CYBERSECURITY AUDIT & ASSURANCE REPORT" in text_content
    assert "Executive Summary" in text_content
