from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.models import Change, ChangeStatus, User, Notification, AuditLog
from app.schemas.schemas import ChangeCreate, ChangeUpdate, ChangeResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/changes", tags=["Change Management"])

@router.get("", response_model=List[ChangeResponse])
def get_changes(status: Optional[str] = None, change_type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Change)
    if status:
        q = q.filter(Change.status == status)
    if change_type:
        q = q.filter(Change.change_type == change_type)
    return q.order_by(desc(Change.id)).all()

@router.post("", response_model=ChangeResponse)
def create_change(
    chg_in: ChangeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    count = db.query(Change).count() + 4001
    c_num = f"CHG-{count}"
    
    chg = Change(
        change_number=c_num,
        title=chg_in.title,
        change_type=chg_in.change_type,
        status=ChangeStatus.REQUESTED,
        requester_name=chg_in.requester_name or current_user.full_name,
        assigned_team=chg_in.assigned_team,
        description=chg_in.description,
        reason_for_change=chg_in.reason_for_change,
        risk_level=chg_in.risk_level,
        impact_level=chg_in.impact_level,
        implementation_plan=chg_in.implementation_plan,
        rollback_plan=chg_in.rollback_plan,
        test_plan=chg_in.test_plan,
        scheduled_start=chg_in.scheduled_start,
        scheduled_end=chg_in.scheduled_end,
        created_at=datetime.now(timezone.utc)
    )
    db.add(chg)
    db.flush()

    db.add(Notification(
        title=f"Change RFC Created: {c_num}",
        message=f"{chg_in.title} submitted for review.",
        notification_type="Change",
        severity="Info",
        link="/changes"
    ))

    db.add(AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="CHANGE_REQUESTED",
        resource_type="Change",
        resource_id=c_num,
        details=f"Created change request {c_num}: {chg_in.title}"
    ))

    db.commit()
    db.refresh(chg)
    return chg

@router.put("/{id}", response_model=ChangeResponse)
def update_change(
    id: int,
    chg_in: ChangeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chg = db.query(Change).filter(Change.id == id).first()
    if not chg:
        raise HTTPException(status_code=404, detail="Change not found")
        
    now = datetime.now(timezone.utc)
    if chg_in.status:
        chg.status = chg_in.status
        if chg_in.status == ChangeStatus.APPROVAL:
            chg.approver_name = current_user.full_name
            chg.approval_date = now
            db.add(AuditLog(
                user_id=current_user.id,
                username=current_user.username,
                action="CHANGE_APPROVED",
                resource_type="Change",
                resource_id=chg.change_number,
                details=f"Approved change {chg.change_number}"
            ))
            
    if chg_in.title:
        chg.title = chg_in.title
    if chg_in.implementation_plan:
        chg.implementation_plan = chg_in.implementation_plan
    if chg_in.rollback_plan:
        chg.rollback_plan = chg_in.rollback_plan
    if chg_in.actual_start:
        chg.actual_start = chg_in.actual_start
    if chg_in.actual_end:
        chg.actual_end = chg_in.actual_end
        
    chg.updated_at = now
    db.commit()
    db.refresh(chg)
    return chg
