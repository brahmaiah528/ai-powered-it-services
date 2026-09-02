from datetime import datetime, timezone
from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import (
    Incident, IncidentStatus, IncidentPriority, InfrastructureNode, HealthStatus,
    Alert, AlertSeverity, Notification, AuditLog, JiraIssueLink
)
from app.services.jira_service import jira_service
from app.services.devops_service import devops_service

router = APIRouter(prefix="/simulation", tags=["Scenario Simulation"])

SCENARIO_STEPS = [
    {"step": 1, "phase": "Detection", "title": "Infrastructure Telemetry Detects Spike", "detail": "Database-01 CPU metric exceeds 90% threshold (Current: 94.2%)."},
    {"step": 2, "phase": "Alerting", "title": "Automated Alert Created", "detail": "Alert ALT-94201 generated with CRITICAL severity for Database-01."},
    {"step": 3, "phase": "Incident Creation", "title": "P1 Incident Generated", "detail": "Incident INC-1025 logged automatically from alert stream."},
    {"step": 4, "phase": "Prioritization", "title": "Priority Calculated (Impact x Urgency)", "detail": "High Impact x High Urgency = P1 Critical (15min Response SLA, 2hr Resolution SLA)."},
    {"step": 5, "phase": "AI Analysis", "title": "AI Diagnostics Engine Invoked", "detail": "AI parses database telemetry logs and query execution graphs."},
    {"step": 6, "phase": "Root Cause", "title": "AI Identifies Probable Cause", "detail": "AI diagnoses unindexed transaction history query storm causing CPU/lock contention (96.5% confidence)."},
    {"step": 7, "phase": "Runbook Suggestion", "title": "AI Recommends Action Steps", "detail": "Suggested actions: Terminate blocking lock PID sessions, deploy hotfix partial index, scale PgBouncer pool."},
    {"step": 8, "phase": "Notification", "title": "Support Engineer Alerted", "detail": "Broadcast notification dispatched to On-Call SRE and Database Administrators."},
    {"step": 9, "phase": "CMDB Asset Link", "title": "Linked to CMDB Asset AST-5001", "detail": "Incident mapped to asset AST-5001 (PostgreSQL Primary Cluster - Database-01)."},
    {"step": 10, "phase": "Jira Integration", "title": "Jira Issue Automatically Created", "detail": "Created linked Jira ticket ITSM-245: '[INC-1025] Critical Database Server CPU Exceeded 90%'."},
    {"step": 11, "phase": "Assignment", "title": "Assigned to SRE Team in Jira", "detail": "Assigned to Sarah Connor (Senior Database SRE)."},
    {"step": 12, "phase": "Investigation", "title": "Engineer Triaging & Applying Hotfix", "detail": "Engineer terminates deadlocks and authors query optimization patch."},
    {"step": 13, "phase": "GitHub Commit", "title": "Patch Committed to GitHub", "detail": "Commit e9a1b42: 'fix(db): add partial index and connection pool tuning for Database-01' pushed to main."},
    {"step": 14, "phase": "CI/CD Webhook", "title": "GitHub Triggers Jenkins Webhook", "detail": "Jenkins pipeline 'it-service-management-ci-cd' webhook received."},
    {"step": 15, "phase": "Automated Testing", "title": "Jenkins Executes Test Suite", "detail": "Backend & Frontend test stages PASS with 100% test coverage."},
    {"step": 16, "phase": "Docker Build", "title": "Docker Image Built", "detail": "Built optimized Docker container image itsm-backend:e9a1b42."},
    {"step": 17, "phase": "Deployment", "title": "Container Deployed to Production", "detail": "Rolling deployment completed with 0 downtime."},
    {"step": 18, "phase": "Verification", "title": "Monitoring Verifies Health Recovery", "detail": "Database-01 CPU metric normalizes from 94.2% down to 28.4% (Status: Healthy)."},
    {"step": 19, "phase": "Resolution", "title": "Incident Marked Resolved", "detail": "INC-1025 status transitioned from 'In Progress' to 'Resolved'."},
    {"step": 20, "phase": "Documentation", "title": "Resolution Notes Recorded", "detail": "Recorded root cause, SQL migration patch SHA, and validation metrics in incident trail."},
    {"step": 21, "phase": "Jira Synchronization", "title": "Jira Ticket Status Synced", "detail": "Jira issue ITSM-245 status automatically transitioned to 'Done'."},
    {"step": 22, "phase": "SLA Metric Update", "title": "SLA & MTTR Metrics Updated", "detail": "Resolution SLA met (Duration: 32 min vs 120 min allowance; 0 breach)."},
    {"step": 23, "phase": "Operations Dashboard", "title": "Executive Dashboard Updated", "detail": "Dashboard KPI cards, SLA rates, and audit logs reflect complete lifecycle resolution."}
]

@router.get("/scenario/steps")
def get_scenario_steps():
    return {"scenario_name": "Critical Database Failure & DevOps Resolution (INC-1025)", "total_steps": 23, "steps": SCENARIO_STEPS}

@router.post("/scenario/execute-step/{step_number}")
def execute_scenario_step(step_number: int, db: Session = Depends(get_db)):
    """Executes state changes corresponding to each step of the end-to-end scenario."""
    now = datetime.now(timezone.utc)
    
    # 1. Metric spike
    if step_number == 1:
        node = db.query(InfrastructureNode).filter(InfrastructureNode.hostname == "Database-01").first()
        if node:
            node.cpu_usage = 94.2
            node.memory_usage = 88.5
            node.status = HealthStatus.CRITICAL
            db.commit()
        return {"step": 1, "status": "executed", "message": "Database-01 CPU spiked to 94.2% (CRITICAL)"}

    # 2. Alert creation
    elif step_number == 2:
        alert = db.query(Alert).filter(Alert.alert_code == "ALT-94201").first()
        if not alert:
            alert = Alert(
                alert_code="ALT-94201",
                source="Infrastructure Monitoring Engine",
                resource_name="Database-01",
                metric_name="CPU",
                metric_value=94.2,
                threshold_value=90.0,
                severity=AlertSeverity.CRITICAL,
                message="Database-01 CPU exceeded 90% threshold for 5 consecutive minutes.",
                incident_created=True,
                is_acknowledged=False
            )
            db.add(alert)
            db.commit()
        return {"step": 2, "status": "executed", "message": "Critical Alert ALT-94201 created"}

    # 3-7. INC-1025 Incident creation & AI analysis
    elif step_number in [3, 4, 5, 6, 7]:
        inc = db.query(Incident).filter(Incident.incident_number == "INC-1025").first()
        if inc:
            inc.status = IncidentStatus.NEW
            inc.priority = IncidentPriority.P1
            inc.ai_confidence = 96.5
            db.commit()
        return {"step": step_number, "status": "executed", "message": f"INC-1025 configured with AI analysis and P1 priority"}

    # 8-11. Jira integration
    elif step_number in [8, 9, 10, 11]:
        inc = db.query(Incident).filter(Incident.incident_number == "INC-1025").first()
        if inc:
            inc.jira_issue_key = "ITSM-245"
            inc.jira_sync_status = "In Sync"
            inc.status = IncidentStatus.IN_PROGRESS
            db.commit()
        return {"step": step_number, "status": "executed", "message": "Jira ticket ITSM-245 linked and assigned to SRE team"}

    # 13-17. DevOps GitHub -> Jenkins -> Docker
    elif step_number in [13, 14, 15, 16, 17]:
        devops_service.get_github_status()["latest_commit"] = {
            "sha": "e9a1b42",
            "message": "fix(db): add partial index and connection pool tuning for Database-01",
            "author": "Sarah Connor (Senior SRE)",
            "timestamp": "Just now",
            "url": "https://github.com/enterprise-org/it-service-management/commit/e9a1b42"
        }
        return {"step": step_number, "status": "executed", "message": "GitHub commit -> Jenkins 11-stage CI/CD pipeline -> Docker container deployed"}

    # 18. Metric Normalization
    elif step_number == 18:
        node = db.query(InfrastructureNode).filter(InfrastructureNode.hostname == "Database-01").first()
        if node:
            node.cpu_usage = 28.4
            node.memory_usage = 42.1
            node.status = HealthStatus.HEALTHY
            db.commit()
        return {"step": 18, "status": "executed", "message": "Database-01 CPU metric normalized to 28.4% (HEALTHY)"}

    # 19-23. Resolution and Jira Sync
    elif step_number in [19, 20, 21, 22, 23]:
        inc = db.query(Incident).filter(Incident.incident_number == "INC-1025").first()
        if inc:
            inc.status = IncidentStatus.RESOLVED
            inc.resolved_at = now
            inc.resolution_notes = "Applied partial index on incident_history and optimized PgBouncer connection limits. Deployed via Jenkins build #129. Verified Database-01 CPU < 30%."
            inc.root_cause = "Lock contention and sequential table scans during concurrent incident updates."
            inc.jira_sync_status = "In Sync (Done)"
            db.commit()
        return {"step": step_number, "status": "executed", "message": "INC-1025 resolved, Jira ITSM-245 marked Done, SLAs updated"}

    return {"step": step_number, "status": "executed", "message": f"Step {step_number} completed"}

@router.post("/scenario/reset")
def reset_scenario(db: Session = Depends(get_db)):
    """Resets scenario back to initial spike state for re-demonstration."""
    node = db.query(InfrastructureNode).filter(InfrastructureNode.hostname == "Database-01").first()
    if node:
        node.cpu_usage = 78.4
        node.memory_usage = 82.1
        node.status = HealthStatus.WARNING
        
    inc = db.query(Incident).filter(Incident.incident_number == "INC-1025").first()
    if inc:
        inc.status = IncidentStatus.NEW
        inc.resolved_at = None
        inc.resolution_notes = None
        inc.jira_sync_status = "In Sync"
        
    db.commit()
    return {"status": "success", "message": "Critical Scenario reset to initial state."}
