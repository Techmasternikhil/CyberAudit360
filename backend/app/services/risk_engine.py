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
    def extract_criticality(crit_or_asset: Any = "MEDIUM") -> str:
        """Normalizes criticality from an Asset instance, BusinessCriticality enum, or string."""
        if hasattr(crit_or_asset, "business_criticality"):
            crit_or_asset = crit_or_asset.business_criticality
        if hasattr(crit_or_asset, "value"):
            return str(crit_or_asset.value).upper()
        return str(crit_or_asset or "MEDIUM").upper()

    @staticmethod
    def is_finding_unresolved(finding: Any) -> bool:
        """Single source of truth for whether a finding is active and unresolved."""
        status_val = str(getattr(finding, "status", "OPEN"))
        if hasattr(getattr(finding, "status", None), "value"):
            status_val = finding.status.value
        return status_val.upper() not in ("RESOLVED", "CLOSED", "MITIGATED", "FALSE_POSITIVE")

    @staticmethod
    def calculate_finding_risk(finding: Finding, asset_criticality: Any = "MEDIUM") -> float:
        likelihood = finding.likelihood if finding.likelihood is not None else 3
        impact = finding.impact if finding.impact is not None else 3
        base_score = finding.cvss_score if finding.cvss_score is not None else (likelihood * impact) / 2.5
        
        # Exposure and KEV penalty
        exposure_multiplier = 1.3 if finding.internet_exposed else 1.0
        kev_multiplier = 1.5 if finding.kev_status else 1.0

        crit_key = RiskEngine.extract_criticality(asset_criticality)
        asset_mult = RiskEngine.CRITICALITY_MULTIPLIER.get(crit_key, 1.0)
        
        final_risk = base_score * exposure_multiplier * kev_multiplier * asset_mult
        
        # Normalize to 0-10 (assuming max theoretical score could exceed 10)
        return min(round(final_risk, 1), 10.0)

    @staticmethod
    def calculate_overall_security_score(findings: list[Finding]) -> Dict[str, Any]:
        """Calculates a 0-100 security score."""
        score = 100
        
        def is_unresolved_severity(f, target_sev: str) -> bool:
            sev = str(getattr(f.severity, "value", f.severity)).upper()
            return sev == target_sev and RiskEngine.is_finding_unresolved(f)

        critical_count = sum(1 for f in findings if is_unresolved_severity(f, "CRITICAL"))
        high_count = sum(1 for f in findings if is_unresolved_severity(f, "HIGH"))
        medium_count = sum(1 for f in findings if is_unresolved_severity(f, "MEDIUM"))
        
        penalties = (critical_count * 15) + (high_count * 5) + (medium_count * 2)
        score -= penalties
        
        score = max(0, score) # Floor at 0
        
        explanation = f"Security score reduced by:\n- {critical_count} critical findings\n- {high_count} high findings\n- {medium_count} medium findings"
        
        return {
            "score": score,
            "explanation": explanation
        }
