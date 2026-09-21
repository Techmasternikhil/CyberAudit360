import pytest
import hashlib
from app.services.evidence_service import EvidenceService

def test_evidence_hash_calculation():
    test_data = b"CyberAudit360-Cryptographic-Integrity-Payload"
    expected_hash = hashlib.sha256(test_data).hexdigest()
    calculated_hash = EvidenceService.calculate_hash(test_data)
    
    assert calculated_hash == expected_hash
    assert len(calculated_hash) == 64
    assert isinstance(calculated_hash, str)

def test_create_evidence_record_with_content():
    content = b"sample network scan output"
    record = EvidenceService.create_evidence_record(
        evidence_type="SCAN_RESULT",
        source="127.0.0.1",
        description="Local socket probe",
        collector="TestCollector",
        content=content
    )
    
    assert record["evidence_type"] == "SCAN_RESULT"
    assert record["source"] == "127.0.0.1"
    assert record["collector"] == "TestCollector"
    assert record["integrity_status"] == "VERIFIED"
    assert record["hash_value"] == hashlib.sha256(content).hexdigest()
    assert "timestamp" in record

def test_create_evidence_record_without_content():
    record = EvidenceService.create_evidence_record(
        evidence_type="MANUAL_OBSERVATION",
        source="Auditor Inspection",
        description="Physical badge reader verification",
        collector="Auditor Jane",
        content=None
    )
    
    assert record["hash_value"] is None
    assert record["integrity_status"] == "VERIFIED"
