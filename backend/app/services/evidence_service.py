import hashlib
from datetime import datetime, timezone
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
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "description": description,
            "hash_value": EvidenceService.calculate_hash(content) if content else None,
            "integrity_status": "VERIFIED"
        }
        return record

    @staticmethod
    def create_evidence_model(
        evidence_type: Any,
        source: str,
        collector: str,
        description: str,
        content: bytes = None,
        hash_value: str = None,
        related_control: str = None,
        id: str = None
    ):
        """Unified factory creating an Evidence ORM model instance with SHA-256 hash."""
        from app.models.evidence import Evidence, EvidenceType
        import uuid

        final_hash = hash_value
        if not final_hash:
            if content:
                final_hash = EvidenceService.calculate_hash(content)
            else:
                seed = f"{description}:{source}".encode("utf-8")
                final_hash = EvidenceService.calculate_hash(seed)

        ev_type = evidence_type
        if isinstance(evidence_type, str):
            ev_type = getattr(EvidenceType, evidence_type, EvidenceType.SCAN_RESULT)

        return Evidence(
            id=id or str(uuid.uuid4()),
            evidence_type=ev_type,
            source=source,
            collector=collector,
            description=description,
            hash_value=final_hash,
            related_control=related_control,
            integrity_status="VERIFIED"
        )
