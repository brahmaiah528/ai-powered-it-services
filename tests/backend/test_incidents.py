import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_incidents():
    response = client.get("/api/incidents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 30

def test_create_incident_with_ai_and_sla():
    payload = {
        "title": "PostgreSQL slow query on payment gateway",
        "description": "Database query timeout during checkout. Latency > 4000ms.",
        "category": "Database",
        "impact": "High",
        "urgency": "High",
        "affected_service": "Payment Microservice"
    }
    response = client.post("/api/incidents", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "P1"
    assert data["category"] == "Database"
    assert data["ai_probable_cause"] is not None
    assert data["ai_confidence"] > 80.0
    assert data["incident_number"].startswith("INC-")

def test_incident_lifecycle_resolve():
    # Fetch first incident
    inc_res = client.get("/api/incidents")
    inc_id = inc_res.json()[0]["id"]
    
    # Resolve
    res = client.post(f"/api/incidents/{inc_id}/resolve", json={
        "resolution_notes": "Killed deadlocked transaction and scaled memory.",
        "root_cause": "Unindexed table scan"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "Resolved"
    assert data["resolution_notes"] is not None
