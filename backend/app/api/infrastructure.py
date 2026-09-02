from datetime import datetime, timezone
import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.models import InfrastructureNode, Alert, HealthStatus
from app.schemas.schemas import (
    InfrastructureNodeResponse, MetricSpikeSimulation, AlertResponse
)
from app.services.alert_service import alert_service

router = APIRouter(prefix="/infrastructure", tags=["Infrastructure Monitoring"])

@router.get("", response_model=List[InfrastructureNodeResponse])
def get_infrastructure_nodes(db: Session = Depends(get_db)):
    nodes = db.query(InfrastructureNode).all()
    # Add subtle dynamic jitter to simulate live monitoring
    for node in nodes:
        if node.status == HealthStatus.HEALTHY:
            node.cpu_usage = max(10.0, min(80.0, node.cpu_usage + random.uniform(-1.5, 1.5)))
            node.memory_usage = max(20.0, min(80.0, node.memory_usage + random.uniform(-0.8, 0.8)))
            node.response_time_ms = max(2.0, min(50.0, node.response_time_ms + random.uniform(-1.0, 1.0)))
    db.commit()
    return nodes

@router.post("/simulate-spike")
def simulate_metric_spike(spike: MetricSpikeSimulation, db: Session = Depends(get_db)):
    """
    Simulates a sudden metric spike on a server/database node.
    If value >= 90%, automatically triggers Alert -> Incident -> AI Analysis -> Notification -> Jira creation.
    """
    result = alert_service.process_metric_update(
        hostname=spike.hostname,
        metric=spike.metric,
        value=spike.value,
        db=db
    )
    return result

@router.post("/normalize/{hostname}")
def normalize_node_metrics(hostname: str, db: Session = Depends(get_db)):
    """Resets node metrics back to healthy state after resolution / container deployment."""
    node = db.query(InfrastructureNode).filter(InfrastructureNode.hostname == hostname).first()
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
        
    node.cpu_usage = 28.4
    node.memory_usage = 42.1
    node.status = HealthStatus.HEALTHY
    node.response_time_ms = 14.2
    node.last_ping = datetime.now(timezone.utc)
    db.commit()
    return {"status": "success", "message": f"{hostname} metrics normalized to healthy state."}

@router.get("/alerts", response_model=List[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(desc(Alert.id)).all()

@router.post("/alerts/{id}/acknowledge")
def acknowledge_alert(id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_acknowledged = True
    db.commit()
    return {"status": "success", "message": f"Alert {alert.alert_code} acknowledged"}
