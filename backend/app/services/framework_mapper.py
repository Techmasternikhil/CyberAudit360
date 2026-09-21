from typing import Dict, List, Any
from app.models.finding import Finding

class FrameworkMapper:
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
    def calculate_coverage(findings: List[Finding]) -> Dict[str, float]:
        """Calculates simulated coverage percentage (demo logic)."""
        # In a real app, this would assess PASSED controls against total framework controls.
        # This is a simplified demo representation.
        base_coverage = 100.0
        penalty = len(findings) * 2.5
        
        return {
            "NIST CSF 2.0": max(0, min(100, base_coverage - penalty)),
            "CIS Controls v8.1": max(0, min(100, base_coverage - (penalty * 1.1))),
            "ISO 27001": max(0, min(100, base_coverage - (penalty * 0.9)))
        }
