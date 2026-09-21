from app.models.finding import Finding
from typing import Dict, Any

class RiskEngine:
    """
    Transparent risk engine that calculates a 0-100 score.
    Weights and factors:
    Technical Severity (CVSS based, 1-10)
    Likelihood (1-5)
    Impact (1-5)
    Asset Criticality multiplier
    Exposure (internet exposed = +risk)
    KEV Status (known exploited = max risk)
    """

    CRITICALITY_MULTIPLIER = {
        "CRITICAL": 1.5,
        "HIGH": 1.2,
        "MEDIUM": 1.0,
        "LOW": 0.8
    }

    @staticmethod
    def calculate_finding_risk(finding: Finding, asset_criticality: str = "MEDIUM") -> float:
        likelihood = finding.likelihood if finding.likelihood is not None else 3
        impact = finding.impact if finding.impact is not None else 3
        base_score = finding.cvss_score if finding.cvss_score is not None else (likelihood * impact) / 2.5
        
        # Exposure and KEV penalty
        exposure_multiplier = 1.3 if finding.internet_exposed else 1.0
        kev_multiplier = 1.5 if finding.kev_status else 1.0

        asset_mult = RiskEngine.CRITICALITY_MULTIPLIER.get(asset_criticality, 1.0)
        
        final_risk = base_score * exposure_multiplier * kev_multiplier * asset_mult
        
        # Normalize to 0-10 (assuming max theoretical score could exceed 10)
        return min(round(final_risk, 1), 10.0)

    @staticmethod
    def calculate_overall_security_score(findings: list[Finding]) -> Dict[str, Any]:
        """Calculates a 0-100 security score."""
        score = 100
        
        critical_count = sum(1 for f in findings if f.severity == "CRITICAL" and f.status != "RESOLVED")
        high_count = sum(1 for f in findings if f.severity == "HIGH" and f.status != "RESOLVED")
        medium_count = sum(1 for f in findings if f.severity == "MEDIUM" and f.status != "RESOLVED")
        
        penalties = (critical_count * 15) + (high_count * 5) + (medium_count * 2)
        score -= penalties
        
        score = max(0, score) # Floor at 0
        
        explanation = f"Security score reduced by:\n- {critical_count} critical findings\n- {high_count} high findings\n- {medium_count} medium findings"
        
        return {
            "score": score,
            "explanation": explanation
        }
