from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "project" in response.json()

def test_get_findings_and_score():
    response = client.get("/api/findings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    score_res = client.get("/api/score")
    assert score_res.status_code == 200
    assert "score" in score_res.json()
    assert 0 <= score_res.json()["score"] <= 100

def test_scan_endpoint():
    response = client.post("/api/scan")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "asset" in data
    assert "total_open_ports" in data
