import pytest
from app.services.risk_engine import RiskEngine
from app.models.finding import Finding
from app.models.asset import Asset

def test_calculate_finding_risk():
    finding = Finding(cvss_score=8.0, kev_status=True, internet_exposed=True)
    # asset_criticality = "HIGH"
    risk_score = RiskEngine.calculate_finding_risk(finding, asset_criticality="HIGH")
    # Base = 8.0, KEV = 1.5, Exposed = 1.3, Criticality = 1.2 -> 8.0 * 1.5 * 1.3 * 1.2 = 18.72, capped at 10.0
    assert risk_score == 10.0
    
    finding2 = Finding(cvss_score=5.0, kev_status=False, internet_exposed=False)
    risk_score2 = RiskEngine.calculate_finding_risk(finding2, asset_criticality="LOW")
    # Base = 5.0, KEV = 1.0, Exposed = 1.0, Criticality = 0.8 -> 5.0 * 0.8 = 4.0
    assert risk_score2 == 4.0

def test_calculate_overall_security_score():
    findings = [
        Finding(severity="CRITICAL", status="OPEN"),
        Finding(severity="HIGH", status="OPEN"),
        Finding(severity="MEDIUM", status="OPEN")
    ]
    # Penalties: Critical(1) = 15, High(1) = 5, Medium(1) = 2. Total penalty = 22
    # Score = 100 - 22 = 78
    result = RiskEngine.calculate_overall_security_score(findings)
    assert result["score"] == 78
    
    # Empty findings
    assert RiskEngine.calculate_overall_security_score([])["score"] == 100
