from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.core.database import get_db
from app.models.models import (
    Incident, IncidentHistory, Comment, User, Asset, Department,
    IncidentStatus, IncidentPriority, Notification, AuditLog
)
from app.schemas.schemas import (
    IncidentCreate, IncidentUpdate, IncidentResponse, IncidentAssign,
    IncidentResolve, CommentCreate, CommentResponse, IncidentHistoryResponse
)
from app.services.sla_service import calculate_priority, calculate_sla_deadlines, check_sla_breaches
from app.services.ai_service import ai_service
from app.api.auth import get_current_user

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=List[IncidentResponse])
def get_incidents(
    priority: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    department_id: Optional[int] = None,
    assigned_technician_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Incident)
    
    if priority:
        query = query.filter(Incident.priority == priority)
    if status:
        query = query.filter(Incident.status == status)
    if category:
        query = query.filter(Incident.category == category)
    if department_id:
        query = query.filter(Incident.department_id == department_id)
    if assigned_technician_id:
        query = query.filter(Incident.assigned_technician_id == assigned_technician_id)
        
    if search:
        s = f"%{search}%"
        query = query.filter(
            or_(
                Incident.incident_number.ilike(s),
                Incident.title.ilike(s),
                Incident.description.ilike(s),
                Incident.affected_service.ilike(s),
                Incident.jira_issue_key.ilike(s)
            )
        )
        
    incidents = query.order_by(desc(Incident.id)).all()
    
    # Check SLAs and construct response
    results = []
    for inc in incidents:
        resp_b, res_b = check_sla_breaches(inc)
        if resp_b != inc.sla_response_breached or res_b != inc.sla_resolution_breached:
            inc.sla_response_breached = resp_b
            inc.sla_resolution_breached = res_b
            db.commit()
            
        results.append(IncidentResponse(
            id=inc.id,
            incident_number=inc.incident_number,
            title=inc.title,
            description=inc.description,
            category=inc.category,
            impact=inc.impact,
            urgency=inc.urgency,
            priority=inc.priority,
            status=inc.status,
            reporter_id=inc.reporter_id,
            reporter_name=inc.reporter.full_name if inc.reporter else None,
            assigned_technician_id=inc.assigned_technician_id,
            assigned_technician_name=inc.assigned_technician.full_name if inc.assigned_technician else None,
            department_id=inc.department_id,
            department_name=inc.department.name if inc.department else None,
            affected_service=inc.affected_service,
            asset_id=inc.asset_id,
            asset_name=inc.asset.asset_name if inc.asset else None,
            sla_response_due=inc.sla_response_due,
            sla_resolution_due=inc.sla_resolution_due,
            responded_at=inc.responded_at,
            resolved_at=inc.resolved_at,
            closed_at=inc.closed_at,
            sla_response_breached=inc.sla_response_breached,
            sla_resolution_breached=inc.sla_resolution_breached,
            ai_probable_cause=inc.ai_probable_cause,
            ai_recommendations=inc.ai_recommendations,
            ai_confidence=inc.ai_confidence,
            ai_suggested_kb_ids=inc.ai_suggested_kb_ids,
            ai_similar_incidents=inc.ai_similar_incidents,
            resolution_notes=inc.resolution_notes,
            root_cause=inc.root_cause,
            jira_issue_key=inc.jira_issue_key,
            jira_sync_status=inc.jira_sync_status,
            jira_issue_url=inc.jira_issue_url,
            created_at=inc.created_at,
            updated_at=inc.updated_at,
            comments_count=len(inc.comments)
        ))
    return results

@router.post("", response_model=IncidentResponse)
def create_incident(
    inc_in: IncidentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    
    # 1. Generate Incident Number
    count = db.query(Incident).count() + 1001
    incident_number = f"INC-{count}"
    
    # 2. Priority Calculation (Impact x Urgency)
    priority = calculate_priority(inc_in.impact, inc_in.urgency)
    
    # 3. AI Analysis & Diagnostics
    ai_diag = ai_service.analyze_incident(
        title=inc_in.title,
        description=inc_in.description,
        category=inc_in.category,
        impact=inc_in.impact,
        urgency=inc_in.urgency,
        db=db
    )
    detected_cat = inc_in.category or ai_diag["suggested_category"]
    
    # 4. Calculate SLAs
    resp_due, res_due = calculate_sla_deadlines(priority, now)
    
    # 5. Create Incident record
    incident = Incident(
        incident_number=incident_number,
        title=inc_in.title,
        description=inc_in.description,
        category=detected_cat,
        impact=inc_in.impact,
        urgency=inc_in.urgency,
        priority=priority,
        status=IncidentStatus.NEW,
        reporter_id=current_user.id,
        assigned_technician_id=inc_in.assigned_technician_id,
        department_id=inc_in.department_id or current_user.department_id,
        affected_service=inc_in.affected_service,
        asset_id=inc_in.asset_id,
        sla_response_due=resp_due,
        sla_resolution_due=res_due,
        ai_probable_cause=ai_diag["probable_cause"],
        ai_recommendations="\n".join([f"{i+1}. {step}" for i, step in enumerate(ai_diag["recommended_actions"])]),
        ai_confidence=ai_diag["confidence_score"],
        ai_suggested_kb_ids=", ".join([kb["article_number"] for kb in ai_diag["relevant_kb_articles"]]),
        ai_similar_incidents=", ".join([sim["incident_number"] for sim in ai_diag["similar_incidents"]])
    )
    
    if inc_in.assigned_technician_id:
        incident.status = IncidentStatus.ASSIGNED
        incident.responded_at = now
        
    db.add(incident)
    db.flush()

    # 6. Add History Entry
    history = IncidentHistory(
        incident_id=incident.id,
        action="INCIDENT_CREATED",
        field_changed="status",
        old_value="None",
        new_value=incident.status.value,
        actor_name=current_user.full_name
    )
    db.add(history)

    # 7. Notification
    notif = Notification(
        title=f"New Incident: {incident_number} ({priority.value})",
        message=f"{inc_in.title} logged by {current_user.full_name}.",
        notification_type="Incident",
        severity="Warning" if priority in [IncidentPriority.P1, IncidentPriority.P2] else "Info",
        link=f"/incidents/{incident.id}"
    )
    db.add(notif)

    # 8. Audit Log
    audit = AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="INCIDENT_CREATED",
        resource_type="Incident",
        resource_id=incident_number,
        details=f"Created incident {incident_number} with priority {priority.value}"
    )
    db.add(audit)
    db.commit()
    db.refresh(incident)

    return get_incident_by_id(incident.id, db)

@router.get("/{id}", response_model=IncidentResponse)
def get_incident_by_id(id: int, db: Session = Depends(get_db)):
    inc = db.query(Incident).filter(Incident.id == id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    resp_b, res_b = check_sla_breaches(inc)
    if resp_b != inc.sla_response_breached or res_b != inc.sla_resolution_breached:
        inc.sla_response_breached = resp_b
        inc.sla_resolution_breached = res_b
        db.commit()

    return IncidentResponse(
        id=inc.id,
        incident_number=inc.incident_number,
        title=inc.title,
        description=inc.description,
        category=inc.category,
        impact=inc.impact,
        urgency=inc.urgency,
        priority=inc.priority,
        status=inc.status,
        reporter_id=inc.reporter_id,
        reporter_name=inc.reporter.full_name if inc.reporter else None,
        assigned_technician_id=inc.assigned_technician_id,
        assigned_technician_name=inc.assigned_technician.full_name if inc.assigned_technician else None,
        department_id=inc.department_id,
        department_name=inc.department.name if inc.department else None,
        affected_service=inc.affected_service,
        asset_id=inc.asset_id,
        asset_name=inc.asset.asset_name if inc.asset else None,
        sla_response_due=inc.sla_response_due,
        sla_resolution_due=inc.sla_resolution_due,
        responded_at=inc.responded_at,
        resolved_at=inc.resolved_at,
        closed_at=inc.closed_at,
        sla_response_breached=inc.sla_response_breached,
        sla_resolution_breached=inc.sla_resolution_breached,
        ai_probable_cause=inc.ai_probable_cause,
        ai_recommendations=inc.ai_recommendations,
        ai_confidence=inc.ai_confidence,
        ai_suggested_kb_ids=inc.ai_suggested_kb_ids,
        ai_similar_incidents=inc.ai_similar_incidents,
        resolution_notes=inc.resolution_notes,
        root_cause=inc.root_cause,
        jira_issue_key=inc.jira_issue_key,
        jira_sync_status=inc.jira_sync_status,
        jira_issue_url=inc.jira_issue_url,
        created_at=inc.created_at,
        updated_at=inc.updated_at,
        comments_count=len(inc.comments)
    )

@router.put("/{id}", response_model=IncidentResponse)
def update_incident(
    id: int,
    inc_in: IncidentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.id == id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    now = datetime.now(timezone.utc)
    
    if inc_in.title is not None:
        inc.title = inc_in.title
    if inc_in.description is not None:
        inc.description = inc_in.description
    if inc_in.category is not None:
        inc.category = inc_in.category
    if inc_in.impact is not None:
        inc.impact = inc_in.impact
    if inc_in.urgency is not None:
        inc.urgency = inc_in.urgency
    if inc_in.priority is not None:
        old_p = inc.priority.value
        inc.priority = inc_in.priority
        resp_due, res_due = calculate_sla_deadlines(inc.priority, inc.created_at)
        inc.sla_response_due = resp_due
        inc.sla_resolution_due = res_due
        db.add(IncidentHistory(
            incident_id=inc.id, action="PRIORITY_CHANGED",
            field_changed="priority", old_value=old_p, new_value=inc.priority.value,
            actor_name=current_user.full_name
        ))
    if inc_in.status is not None:
        old_s = inc.status.value
        inc.status = inc_in.status
        if inc_in.status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED] and not inc.resolved_at:
            inc.resolved_at = now
        db.add(IncidentHistory(
            incident_id=inc.id, action="STATUS_CHANGED",
            field_changed="status", old_value=old_s, new_value=inc.status.value,
            actor_name=current_user.full_name
        ))
    if inc_in.assigned_technician_id is not None:
        old_tech = inc.assigned_technician.full_name if inc.assigned_technician else "Unassigned"
        inc.assigned_technician_id = inc_in.assigned_technician_id
        tech = db.query(User).filter(User.id == inc_in.assigned_technician_id).first()
        new_tech = tech.full_name if tech else f"User {inc_in.assigned_technician_id}"
        if inc.status == IncidentStatus.NEW:
            inc.status = IncidentStatus.ASSIGNED
        if not inc.responded_at:
            inc.responded_at = now
        db.add(IncidentHistory(
            incident_id=inc.id, action="INCIDENT_ASSIGNED",
            field_changed="assigned_technician", old_value=old_tech, new_value=new_tech,
            actor_name=current_user.full_name
        ))
    if inc_in.affected_service is not None:
        inc.affected_service = inc_in.affected_service
    if inc_in.asset_id is not None:
        inc.asset_id = inc_in.asset_id
    if inc_in.resolution_notes is not None:
        inc.resolution_notes = inc_in.resolution_notes
    if inc_in.root_cause is not None:
        inc.root_cause = inc_in.root_cause
        
    inc.updated_at = now
    db.commit()
    return get_incident_by_id(inc.id, db)

@router.post("/{id}/assign", response_model=IncidentResponse)
def assign_incident(
    id: int,
    assign_in: IncidentAssign,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_incident(id, IncidentUpdate(assigned_technician_id=assign_in.technician_id), current_user, db)

@router.post("/{id}/resolve", response_model=IncidentResponse)
def resolve_incident(
    id: int,
    res_in: IncidentResolve,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.id == id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    now = datetime.now(timezone.utc)
    old_status = inc.status.value
    inc.status = IncidentStatus.RESOLVED
    inc.resolved_at = now
    inc.resolution_notes = res_in.resolution_notes
    inc.root_cause = res_in.root_cause
    inc.updated_at = now
    
    # History
    db.add(IncidentHistory(
        incident_id=inc.id,
        action="INCIDENT_RESOLVED",
        field_changed="status",
        old_value=old_status,
        new_value=IncidentStatus.RESOLVED.value,
        actor_name=current_user.full_name
    ))

    # Notification
    db.add(Notification(
        title=f"Incident Resolved: {inc.incident_number}",
        message=f"{inc.incident_number} resolved by {current_user.full_name}.",
        notification_type="Incident",
        severity="Success",
        link=f"/incidents/{inc.id}"
    ))

    # Audit
    db.add(AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="INCIDENT_RESOLVED",
        resource_type="Incident",
        resource_id=inc.incident_number,
        details=f"Resolved with notes: {res_in.resolution_notes[:100]}"
    ))

    db.commit()
    return get_incident_by_id(inc.id, db)

@router.post("/{id}/reopen", response_model=IncidentResponse)
def reopen_incident(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.id == id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    old_status = inc.status.value
    inc.status = IncidentStatus.IN_PROGRESS
    inc.resolved_at = None
    inc.closed_at = None
    inc.updated_at = datetime.now(timezone.utc)
    
    db.add(IncidentHistory(
        incident_id=inc.id,
        action="INCIDENT_REOPENED",
        field_changed="status",
        old_value=old_status,
        new_value=IncidentStatus.IN_PROGRESS.value,
        actor_name=current_user.full_name
    ))
    db.commit()
    return get_incident_by_id(inc.id, db)

@router.post("/{id}/close", response_model=IncidentResponse)
def close_incident(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.id == id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    old_status = inc.status.value
    inc.status = IncidentStatus.CLOSED
    inc.closed_at = datetime.now(timezone.utc)
    inc.updated_at = datetime.now(timezone.utc)
    
    db.add(IncidentHistory(
        incident_id=inc.id,
        action="INCIDENT_CLOSED",
        field_changed="status",
        old_value=old_status,
        new_value=IncidentStatus.CLOSED.value,
        actor_name=current_user.full_name
    ))
    db.commit()
    return get_incident_by_id(inc.id, db)

@router.get("/{id}/comments", response_model=List[CommentResponse])
def get_incident_comments(id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.incident_id == id).order_by(Comment.created_at.asc()).all()

@router.post("/{id}/comments", response_model=CommentResponse)
def add_incident_comment(
    id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    inc = db.query(Incident).filter(Incident.id == id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    c = Comment(
        incident_id=inc.id,
        author_name=current_user.full_name,
        author_role=current_user.role.value,
        content=comment_in.content,
        is_internal=comment_in.is_internal
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/{id}/history", response_model=List[IncidentHistoryResponse])
def get_incident_history(id: int, db: Session = Depends(get_db)):
    return db.query(IncidentHistory).filter(IncidentHistory.incident_id == id).order_by(desc(IncidentHistory.timestamp)).all()
