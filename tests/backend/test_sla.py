import sys
import os
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend")))

from app.models.models import IncidentPriority
from app.services.sla_service import calculate_priority, calculate_sla_deadlines

def test_priority_matrix():
    assert calculate_priority("High", "High") == IncidentPriority.P1
    assert calculate_priority("High", "Medium") == IncidentPriority.P2
    assert calculate_priority("Medium", "High") == IncidentPriority.P2
    assert calculate_priority("Medium", "Medium") == IncidentPriority.P3
    assert calculate_priority("Low", "Low") == IncidentPriority.P4

def test_sla_deadlines():
    now = datetime.now(timezone.utc)
    resp_p1, res_p1 = calculate_sla_deadlines(IncidentPriority.P1, now)
    assert (resp_p1 - now).total_seconds() == 15 * 60
    assert (res_p1 - now).total_seconds() == 120 * 60
