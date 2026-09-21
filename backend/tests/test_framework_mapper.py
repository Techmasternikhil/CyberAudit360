import pytest
from app.services.framework_mapper import FrameworkMapper
from app.models.finding import Finding, Severity, FindingStatus

def test_map_finding_known_categories():
    # Firewall
    fw_mapping = FrameworkMapper.map_finding("Host Firewall Disabled", "Local firewall is inactive")
    assert "NIST CSF 2.0" in fw_mapping
    assert "PR.PS-01" in fw_mapping["NIST CSF 2.0"]
    assert "CIS Controls v8.1" in fw_mapping
    assert "4.1" in fw_mapping["CIS Controls v8.1"]

    # RDP
    rdp_mapping = FrameworkMapper.map_finding("Internet-Exposed RDP Service", "Remote desktop accessible")
    assert "ISO 27001" in rdp_mapping
    assert "A.11.2.6" in rdp_mapping["ISO 27001"]

    # Outdated dependency
    dep_mapping = FrameworkMapper.map_finding("Outdated dependency in backend", "Vulnerable package")
    assert "ID.RA-01" in dep_mapping["NIST CSF 2.0"]

def test_map_finding_fallback():
    unknown_mapping = FrameworkMapper.map_finding("Miscellaneous Custom Finding", "No matching pattern")
    assert "NIST CSF 2.0" in unknown_mapping
    assert "CIS Controls v8.1" in unknown_mapping
    assert "ISO 27001" in unknown_mapping

def test_calculate_coverage_all_open():
    findings = [
        Finding(title="F1", description="D1", severity=Severity.HIGH, status=FindingStatus.OPEN),
        Finding(title="F2", description="D2", severity=Severity.MEDIUM, status=FindingStatus.OPEN)
    ]
    coverage = FrameworkMapper.calculate_coverage(findings)
    # 2 open findings -> penalty = 5.0
    assert coverage["NIST CSF 2.0"] == 95.0
    assert coverage["CIS Controls v8.1"] == round(100.0 - (5.0 * 1.1), 1)
    assert coverage["ISO 27001"] == round(100.0 - (5.0 * 0.9), 1)

def test_calculate_coverage_resolved_findings():
    findings = [
        Finding(title="F1", description="D1", severity=Severity.HIGH, status=FindingStatus.RESOLVED),
        Finding(title="F2", description="D2", severity=Severity.MEDIUM, status=FindingStatus.RESOLVED)
    ]
    coverage = FrameworkMapper.calculate_coverage(findings)
    # 0 open findings -> penalty = 0.0 -> coverage = 100%
    assert coverage["NIST CSF 2.0"] == 100.0
    assert coverage["CIS Controls v8.1"] == 100.0
    assert coverage["ISO 27001"] == 100.0
