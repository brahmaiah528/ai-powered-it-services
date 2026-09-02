import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ai_incident_classification_and_recommendations():
    payload = {
        "title": "VPN gateway packet loss and session drops",
        "description": "AnyConnect VPN clients disconnecting after 5 minutes of usage.",
        "impact": "High",
        "urgency": "Medium"
    }
    response = client.post("/api/ai/analyze-incident", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["suggested_category"] == "Network"
    assert data["calculated_priority"] == "P2"
    assert "VPN" in data["probable_cause"]
    assert len(data["recommended_actions"]) > 0
    assert data["confidence_score"] >= 80.0
