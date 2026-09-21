from typing import Dict, List, Any
from app.models.finding import Finding

class FrameworkMapper:
    SUPPORTED_FRAMEWORKS = ["NIST CSF 2.0", "CIS Controls v8.1", "ISO 27001"]

    # A simplified static mapping for demonstration purposes
    MAPPINGS = {
        "Firewall Disabled": {
            "NIST CSF 2.0": ["PR.PS-01", "PR.IR-01"],
            "CIS Controls v8.1": ["4.1", "4.2"],
            "ISO 27001": ["A.13.1.1"]
        },
        "Internet-Exposed RDP": {
            "NIST CSF 2.0": ["PR.AC-03", "PR.PT-04"],
            "CIS Controls v8.1": ["12.1", "12.4"],
            "ISO 27001": ["A.11.2.6"]
        },
        "Outdated dependency": {
            "NIST CSF 2.0": ["ID.RA-01", "PR.IP-12"],
            "CIS Controls v8.1": ["7.1", "7.3"],
            "ISO 27001": ["A.12.6.1"]
        }
    }

    @staticmethod
    def map_finding(title: str, description: str) -> Dict[str, List[str]]:
        """Maps a finding title/description to compliance frameworks."""
        for key, mapping in FrameworkMapper.MAPPINGS.items():
            if key.lower() in title.lower() or key.lower() in description.lower():
                return mapping
        
        # Default fallback map
        return {
            "NIST CSF 2.0": ["PR.IP-01"],
            "CIS Controls v8.1": ["3.1"],
            "ISO 27001": ["A.8.1.1"]
        }

    @staticmethod
    def format_mappings(mappings: Dict[str, List[str]], separator: str = " | ") -> str:
        """Standardized string formatter for framework mappings."""
        return separator.join([f"{fw}: {', '.join(ctrls)}" for fw, ctrls in mappings.items()])

    @staticmethod
    def calculate_coverage(findings: List[Finding]) -> Dict[str, float]:
        """Calculates framework coverage percentage based on active/unresolved findings."""
        base_coverage = 100.0
        from app.services.risk_engine import RiskEngine
        open_findings = [f for f in findings if RiskEngine.is_finding_unresolved(f)]
        penalty = len(open_findings) * 2.5
        
        return {
            "NIST CSF 2.0": round(max(0.0, min(100.0, base_coverage - penalty)), 1),
            "CIS Controls v8.1": round(max(0.0, min(100.0, base_coverage - (penalty * 1.1))), 1),
            "ISO 27001": round(max(0.0, min(100.0, base_coverage - (penalty * 0.9))), 1)
        }
