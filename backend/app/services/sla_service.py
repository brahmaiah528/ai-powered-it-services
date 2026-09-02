from datetime import datetime, timedelta, timezone
from typing import Tuple
from app.models.models import IncidentPriority

# Standard Enterprise SLA Matrix:
# P1: Response SLA = 15m, Resolution SLA = 2h (120m)
# P2: Response SLA = 30m, Resolution SLA = 4h (240m)
# P3: Response SLA = 2h (120m), Resolution SLA = 8h (480m)
# P4: Response SLA = 8h (480m), Resolution SLA = 24h (1440m)
SLA_CONFIG = {
    IncidentPriority.P1: {"response_min": 15, "resolution_min": 120},
    IncidentPriority.P2: {"response_min": 30, "resolution_min": 240},
    IncidentPriority.P3: {"response_min": 120, "resolution_min": 480},
    IncidentPriority.P4: {"response_min": 480, "resolution_min": 1440},
}

def calculate_priority(impact: str, urgency: str) -> IncidentPriority:
    """
    Priority = Impact x Urgency
    High + High = P1
    High + Medium / Medium + High = P2
    Medium + Medium / High + Low / Low + High = P3
    Low + Low / Medium + Low / Low + Medium = P4
    """
    imp = (impact or "Medium").capitalize()
    urg = (urgency or "Medium").capitalize()
    
    if imp == "High" and urg == "High":
        return IncidentPriority.P1
    elif (imp == "High" and urg == "Medium") or (imp == "Medium" and urg == "High"):
        return IncidentPriority.P2
    elif (imp == "Medium" and urg == "Medium") or (imp == "High" and urg == "Low") or (imp == "Low" and urg == "High"):
        return IncidentPriority.P3
    else:
        return IncidentPriority.P4

def calculate_sla_deadlines(priority: IncidentPriority, created_at: datetime = None) -> Tuple[datetime, datetime]:
    if not created_at:
        created_at = datetime.now(timezone.utc)
    
    # Ensure timezone aware
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
        
    cfg = SLA_CONFIG.get(priority, SLA_CONFIG[IncidentPriority.P3])
    response_due = created_at + timedelta(minutes=cfg["response_min"])
    resolution_due = created_at + timedelta(minutes=cfg["resolution_min"])
    return response_due, resolution_due

def check_sla_breaches(incident) -> Tuple[bool, bool]:
    now = datetime.now(timezone.utc)
    
    # Response breach check
    response_breached = incident.sla_response_breached
    if not response_breached and incident.sla_response_due:
        resp_due = incident.sla_response_due.replace(tzinfo=timezone.utc) if incident.sla_response_due.tzinfo is None else incident.sla_response_due
        if incident.responded_at is None and now > resp_due:
            response_breached = True
            
    # Resolution breach check
    resolution_breached = incident.sla_resolution_breached
    if not resolution_breached and incident.sla_resolution_due:
        res_due = incident.sla_resolution_due.replace(tzinfo=timezone.utc) if incident.sla_resolution_due.tzinfo is None else incident.sla_resolution_due
        if incident.resolved_at is None and now > res_due:
            resolution_breached = True
            
    return response_breached, resolution_breached
