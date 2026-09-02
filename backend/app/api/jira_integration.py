from datetime import datetime, timezone
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Incident, JiraIssueLink, AuditLog, Notification
from app.schemas.schemas import JiraCreateIssueRequest, JiraIssueResponse
from app.services.jira_service import jira_service
from app.api.auth import get_current_user

router = APIRouter(prefix="/jira", tags=["Jira Integration"])

@router.get("/issues")
def get_jira_issues(db: Session = Depends(get_db)):
    links = db.query(JiraIssueLink).all()
    # Also include mock issues in memory
    res = []
    for link in links:
        res.append({
            "jira_key": link.jira_key,
            "incident_number": link.incident_number,
            "summary": link.jira_summary,
            "status": link.jira_status,
            "priority": link.jira_priority,
            "assignee": link.jira_assignee,
            "url": f"https://company-itsm.atlassian.net/browse/{link.jira_key}",
            "last_synced": link.last_synced
        })
    # Add any in-memory mock issues not in DB
    for key, data in jira_service.mock_issues.items():
        if not any(r["jira_key"] == key for r in res):
            res.append({
                "jira_key": data["key"],
                "incident_number": data.get("incident_number", "INC-1025"),
                "summary": data["summary"],
                "status": data["status"],
                "priority": data["priority"],
                "assignee": data["assignee"],
                "url": data["url"],
                "last_synced": datetime.now(timezone.utc)
            })
    return res

@router.post("/create-issue", response_model=JiraIssueResponse)
async def create_jira_issue(
    req: JiraCreateIssueRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.incident_number == req.incident_number).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    summary = req.summary or inc.title
    description = req.description or inc.description
    
    jira_res = await jira_service.create_issue(
        incident_number=inc.incident_number,
        summary=summary,
        description=description,
        priority=inc.priority.value,
        issue_type=req.issue_type
    )
    
    key = jira_res["jira_key"]
    inc.jira_issue_key = key
    inc.jira_sync_status = jira_res["sync_status"]
    inc.jira_issue_url = jira_res["url"]
    
    # Save link in DB
    link = db.query(JiraIssueLink).filter(JiraIssueLink.incident_number == inc.incident_number).first()
    if not link:
        link = JiraIssueLink(
            incident_number=inc.incident_number,
            jira_key=key,
            jira_summary=summary,
            jira_status=jira_res["status"],
            jira_priority=jira_res["priority"],
            jira_assignee="Enterprise SRE On-Call Team",
            last_synced=datetime.now(timezone.utc)
        )
        db.add(link)
    else:
        link.jira_key = key
        link.jira_summary = summary
        link.last_synced = datetime.now(timezone.utc)
        
    db.add(Notification(
        title=f"Jira Issue Linked: {key}",
        message=f"Incident {inc.incident_number} linked to Jira {key}.",
        notification_type="DevOps",
        severity="Info",
        link="/devops"
    ))

    db.add(AuditLog(
        user_id=current_user.id if hasattr(current_user, 'id') else 1,
        username=current_user.username if hasattr(current_user, 'username') else 'admin',
        action="JIRA_ISSUE_CREATED",
        resource_type="Jira",
        resource_id=key,
        details=f"Created Jira issue {key} linked to {inc.incident_number}"
    ))

    db.commit()
    return JiraIssueResponse(
        jira_key=key,
        incident_number=inc.incident_number,
        summary=summary,
        status=jira_res["status"],
        priority=jira_res["priority"],
        assignee="Enterprise SRE On-Call Team",
        url=jira_res["url"],
        sync_status=jira_res["sync_status"]
    )

@router.post("/sync/{jira_key}")
async def sync_jira_issue(jira_key: str, db: Session = Depends(get_db)):
    sync_res = await jira_service.sync_issue(jira_key)
    
    # Update linked incident if present
    link = db.query(JiraIssueLink).filter(JiraIssueLink.jira_key == jira_key).first()
    if link:
        link.jira_status = sync_res["status"]
        link.jira_priority = sync_res["priority"]
        link.last_synced = datetime.now(timezone.utc)
        
        inc = db.query(Incident).filter(Incident.incident_number == link.incident_number).first()
        if inc:
            inc.jira_sync_status = sync_res["sync_status"]
            db.commit()

    return sync_res
