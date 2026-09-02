import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_jira_integration_workflow():
    payload = {
        "incident_number": "INC-1025",
        "summary": "Critical Database Server CPU Spike (Simulated)",
        "description": "Database-01 experiencing high load bottleneck.",
        "issue_type": "Bug",
        "priority": "Highest"
    }
    response = client.post("/api/jira/create-issue", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["jira_key"].startswith("ITSM-")
    assert "url" in data
    assert data["sync_status"] is not None

def test_jira_sync_endpoint():
    response = client.post("/api/jira/sync/ITSM-245")
    assert response.status_code == 200
    data = response.json()
    assert data["jira_key"] == "ITSM-245"
    assert "status" in data
