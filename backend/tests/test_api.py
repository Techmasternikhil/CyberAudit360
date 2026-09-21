import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "project" in data

def test_demo_seed_and_reset():
    # Test seeding
    seed_res = client.post("/api/demo/seed")
    assert seed_res.status_code == 200
    assert seed_res.json()["status"] == "success"
    
    # Verify findings and assets exist
    findings_res = client.get("/api/findings")
    assert findings_res.status_code == 200
    assert len(findings_res.json()) > 0
    
    assets_res = client.get("/api/assets")
    assert assets_res.status_code == 200
    assert len(assets_res.json()) > 0

    # Test reset
    reset_res = client.post("/api/demo/reset")
    assert reset_res.status_code == 200
    assert reset_res.json()["status"] == "success"
    
    # Verify findings are empty after reset
    empty_findings = client.get("/api/findings").json()
    assert len(empty_findings) == 0

def test_dashboard_summary():
    # Seed scenario first
    client.post("/api/demo/seed")
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "findings" in data
    assert "assets" in data
    assert "score" in data
    assert "coverage" in data
    assert len(data["findings"]) > 0
    assert len(data["assets"]) > 0
    assert isinstance(data["score"], (int, float))
    assert "NIST CSF 2.0" in data["coverage"]

def test_asset_lifecycle():
    # Create asset
    asset_payload = {
        "hostname": "prod-db-cluster-01",
        "ip_address": "10.0.1.50",
        "os_name": "Linux Ubuntu",
        "os_version": "22.04 LTS",
        "architecture": "x86_64",
        "asset_type": "DATABASE",
        "business_criticality": "CRITICAL",
        "discovery_source": "MANUAL"
    }
    create_res = client.post("/api/assets", json=asset_payload)
    assert create_res.status_code == 200
    asset_data = create_res.json()
    assert asset_data["hostname"] == "prod-db-cluster-01"
    assert "id" in asset_data

    # List assets
    list_res = client.get("/api/assets")
    assert list_res.status_code == 200
    assert any(a["id"] == asset_data["id"] for a in list_res.json())

def test_finding_creation_and_risk_scoring():
    # First create an asset to link to
    asset_res = client.post("/api/assets", json={
        "hostname": "sec-test-host",
        "ip_address": "192.168.1.10",
        "asset_type": "SERVER",
        "business_criticality": "HIGH",
        "discovery_source": "API_TEST"
    })
    asset_id = asset_res.json()["id"]

    # Create finding
    finding_payload = {
        "asset_id": asset_id,
        "title": "Unauthenticated Redis Service Exposed",
        "description": "Port 6379 is accessible without authentication requirement.",
        "category": "Authentication Bypass",
        "severity": "CRITICAL",
        "cvss_score": 9.8,
        "likelihood": 4,
        "impact": 5,
        "kev_status": True,
        "internet_exposed": True,
        "recommendation": "Bind Redis to localhost and configure strong requirepass password."
    }
    post_res = client.post("/api/findings", json=finding_payload)
    assert post_res.status_code == 200
    finding = post_res.json()
    assert finding["title"] == "Unauthenticated Redis Service Exposed"
    assert finding["severity"] == "CRITICAL"
    assert finding["risk_score"] is not None
    # For critical CVSS 9.8 + KEV + exposed + high criticality, risk score caps at 10.0
    assert finding["risk_score"] == 10.0

    # Retrieve by ID
    get_res = client.get(f"/api/findings/{finding['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == finding["id"]

    # Update finding
    patch_res = client.patch(f"/api/findings/{finding['id']}", json={"owner": "SecOps Team"})
    assert patch_res.status_code == 200
    assert patch_res.json()["owner"] == "SecOps Team"

    # Toggle status
    toggle_res = client.patch(f"/api/findings/{finding['id']}/toggle-status")
    assert toggle_res.status_code == 200
    assert toggle_res.json()["new_status"] == "RESOLVED"

    # Toggle back
    toggle_res2 = client.patch(f"/api/findings/{finding['id']}/toggle-status")
    assert toggle_res2.status_code == 200
    assert toggle_res2.json()["new_status"] == "OPEN"

    # Clean up delete
    del_res = client.delete(f"/api/findings/{finding['id']}")
    assert del_res.status_code == 200
    
    # Verify 404 on deleted
    not_found = client.get(f"/api/findings/{finding['id']}")
    assert not_found.status_code == 404

def test_evidence_workflow():
    ev_payload = {
        "evidence_type": "SCAN_RESULT",
        "source": "127.0.0.1:443",
        "collector": "Automated Scanner",
        "description": "TLS 1.0/1.1 protocol handshake detected",
        "related_control": "NIST PR.DS-02"
    }
    post_res = client.post("/api/evidence", json=ev_payload)
    assert post_res.status_code == 200
    ev_data = post_res.json()
    assert "id" in ev_data
    assert ev_data["hash_value"] is not None
    assert len(ev_data["hash_value"]) == 64
    assert ev_data["integrity_status"] == "VERIFIED"

    # List evidence
    list_res = client.get("/api/evidence")
    assert list_res.status_code == 200
    assert any(e["id"] == ev_data["id"] for e in list_res.json())

def test_remediation_workflow():
    # Seed scenario to ensure finding exists
    client.post("/api/demo/seed")
    findings = client.get("/api/findings").json()
    assert len(findings) > 0
    test_finding = findings[0]
    
    # Create remediation
    rem_payload = {
        "finding_id": test_finding["id"],
        "owner": "Infrastructure Lead",
        "action": "Patch vulnerable package to v2.14.1 and verify hash",
        "priority": "HIGH",
        "status": "IN_PROGRESS",
        "notes": "Testing in staging environment first"
    }
    rem_res = client.post(f"/api/findings/{test_finding['id']}/remediation", json=rem_payload)
    assert rem_res.status_code == 200
    rem_data = rem_res.json()
    assert rem_data["finding_id"] == test_finding["id"]
    assert rem_data["owner"] == "Infrastructure Lead"
    assert rem_data["status"] == "IN_PROGRESS"

    # Get single remediation
    get_rem = client.get(f"/api/findings/{test_finding['id']}/remediation")
    assert get_rem.status_code == 200
    assert get_rem.json()["owner"] == "Infrastructure Lead"

    # List all remediations
    all_rems = client.get("/api/remediations")
    assert all_rems.status_code == 200
    assert len(all_rems.json()) > 0

def test_compliance_coverage_endpoint():
    res = client.get("/api/compliance/coverage")
    assert res.status_code == 200
    data = res.json()
    assert "coverage" in data
    assert "NIST CSF 2.0" in data["coverage"]
    assert "CIS Controls v8.1" in data["coverage"]
    assert "ISO 27001" in data["coverage"]
    assert "frameworks" in data
    assert "mapped_findings" in data

def test_live_scan_endpoint():
    res = client.post("/api/scan")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "asset" in data
    assert "total_open_ports" in data
    assert "evidence_id" in data
    assert "evidence_hash" in data
    assert len(data["evidence_hash"]) == 64

def test_report_export_endpoints():
    # DOCX export
    docx_res = client.get("/api/report/export?format=docx")
    assert docx_res.status_code == 200
    assert docx_res.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    assert docx_res.content[:4] == b"PK\x03\x04"

    # Markdown export
    md_res = client.get("/api/report/export?format=md")
    assert md_res.status_code == 200
    assert "text/markdown" in md_res.headers["content-type"]
    assert b"Cybersecurity Audit Report" in md_res.content

def test_error_handling_paths():
    # Non-existent finding 404
    non_existent_id = str(uuid.uuid4())
    res = client.get(f"/api/findings/{non_existent_id}")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()

    # Toggle status on non-existent finding 404
    res_toggle = client.patch(f"/api/findings/{non_existent_id}/toggle-status")
    assert res_toggle.status_code == 404

    # Delete non-existent finding 404
    res_del = client.delete(f"/api/findings/{non_existent_id}")
    assert res_del.status_code == 404

    # Remediation for non-existent finding 404
    rem_payload = {
        "finding_id": non_existent_id,
        "owner": "Nobody",
        "action": "Do nothing"
    }
    res_rem = client.post(f"/api/findings/{non_existent_id}/remediation", json=rem_payload)
    assert res_rem.status_code == 404
