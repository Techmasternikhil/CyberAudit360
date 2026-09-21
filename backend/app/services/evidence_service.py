import hashlib
from datetime import datetime
from typing import Dict, Any

class EvidenceService:
    @staticmethod
    def calculate_hash(content: bytes) -> str:
        """Calculates SHA-256 hash for evidence integrity."""
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def create_evidence_record(evidence_type: str, source: str, description: str, collector: str, content: bytes = None) -> Dict[str, Any]:
        """Creates an evidence record with an optional hash for integrity verification."""
        record = {
            "evidence_type": evidence_type,
            "source": source,
            "collector": collector,
            "timestamp": datetime.utcnow().isoformat(),
            "description": description,
            "hash_value": EvidenceService.calculate_hash(content) if content else None,
            "integrity_status": "VERIFIED"
        }
        return record
