from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.models import Problem, Incident, ProblemStatus, User, AuditLog
from app.schemas.schemas import ProblemCreate, ProblemUpdate, ProblemResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/problems", tags=["Problem Management"])

@router.get("", response_model=List[ProblemResponse])
def get_problems(status: Optional[str] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Problem)
    if status:
        q = q.filter(Problem.status == status)
    if category:
        q = q.filter(Problem.category == category)
    problems = q.order_by(desc(Problem.id)).all()
    
    return [ProblemResponse(
        id=p.id,
        problem_number=p.problem_number,
        title=p.title,
        description=p.description,
        category=p.category,
        status=p.status,
        impact=p.impact,
        root_cause=p.root_cause,
        workaround=p.workaround,
        permanent_solution=p.permanent_solution,
        assigned_team=p.assigned_team,
        created_at=p.created_at,
        updated_at=p.updated_at,
        related_incident_count=len(p.incidents),
        incident_numbers=[inc.incident_number for inc in p.incidents]
    ) for p in problems]

@router.post("", response_model=ProblemResponse)
def create_problem(
    prb_in: ProblemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = db.query(Problem).count() + 3001
    p_num = f"PRB-{count}"
    
    prb = Problem(
        problem_number=p_num,
        title=prb_in.title,
        description=prb_in.description,
        category=prb_in.category,
        status=ProblemStatus.LOGGED,
        impact=prb_in.impact,
        root_cause=prb_in.root_cause,
        workaround=prb_in.workaround,
        permanent_solution=prb_in.permanent_solution,
        assigned_team=prb_in.assigned_team,
        created_at=datetime.now(timezone.utc)
    )
    
    if prb_in.incident_ids:
        incidents = db.query(Incident).filter(Incident.id.in_(prb_in.incident_ids)).all()
        prb.incidents.extend(incidents)
        
    db.add(prb)
    db.flush()

    db.add(AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="PROBLEM_CREATED",
        resource_type="Problem",
        resource_id=p_num,
        details=f"Logged problem record {p_num}: {prb_in.title}"
    ))

    db.commit()
    db.refresh(prb)
    
    return ProblemResponse(
        id=prb.id,
        problem_number=prb.problem_number,
        title=prb.title,
        description=prb.description,
        category=prb.category,
        status=prb.status,
        impact=prb.impact,
        root_cause=prb.root_cause,
        workaround=prb.workaround,
        permanent_solution=prb.permanent_solution,
        assigned_team=prb.assigned_team,
        created_at=prb.created_at,
        updated_at=prb.updated_at,
        related_incident_count=len(prb.incidents),
        incident_numbers=[inc.incident_number for inc in prb.incidents]
    )

@router.put("/{id}", response_model=ProblemResponse)
def update_problem(
    id: int,
    prb_in: ProblemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prb = db.query(Problem).filter(Problem.id == id).first()
    if not prb:
        raise HTTPException(status_code=404, detail="Problem not found")
        
    if prb_in.title:
        prb.title = prb_in.title
    if prb_in.description:
        prb.description = prb_in.description
    if prb_in.status:
        prb.status = prb_in.status
    if prb_in.root_cause:
        prb.root_cause = prb_in.root_cause
    if prb_in.workaround:
        prb.workaround = prb_in.workaround
    if prb_in.permanent_solution:
        prb.permanent_solution = prb_in.permanent_solution
    if prb_in.assigned_team:
        prb.assigned_team = prb_in.assigned_team
        
    if prb_in.incident_ids is not None:
        incidents = db.query(Incident).filter(Incident.id.in_(prb_in.incident_ids)).all()
        prb.incidents = incidents
        
    prb.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(prb)
    
    return ProblemResponse(
        id=prb.id,
        problem_number=prb.problem_number,
        title=prb.title,
        description=prb.description,
        category=prb.category,
        status=prb.status,
        impact=prb.impact,
        root_cause=prb.root_cause,
        workaround=prb.workaround,
        permanent_solution=prb.permanent_solution,
        assigned_team=prb.assigned_team,
        created_at=prb.created_at,
        updated_at=prb.updated_at,
        related_incident_count=len(prb.incidents),
        incident_numbers=[inc.incident_number for inc in prb.incidents]
    )
