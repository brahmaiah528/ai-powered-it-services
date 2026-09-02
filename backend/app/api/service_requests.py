from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.models import ServiceRequest, ServiceRequestStatus, User, Notification, AuditLog
from app.schemas.schemas import ServiceRequestCreate, ServiceRequestUpdate, ServiceRequestResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/service-requests", tags=["Service Requests"])

@router.get("", response_model=List[ServiceRequestResponse])
def get_service_requests(
    status: Optional[str] = None,
    request_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(ServiceRequest)
    if status:
        q = q.filter(ServiceRequest.status == status)
    if request_type:
        q = q.filter(ServiceRequest.request_type == request_type)
    reqs = q.order_by(desc(ServiceRequest.id)).all()
    
    return [ServiceRequestResponse(
        id=r.id,
        request_number=r.request_number,
        title=r.title,
        request_type=r.request_type,
        description=r.description,
        urgency=r.urgency,
        status=r.status,
        requester_id=r.requester_id,
        requester_name=r.requester.full_name if r.requester else None,
        assigned_to=r.assigned_to,
        approval_required=r.approval_required,
        approver_name=r.approver_name,
        approval_notes=r.approval_notes,
        sla_due=r.sla_due,
        completed_at=r.completed_at,
        created_at=r.created_at,
        updated_at=r.updated_at
    ) for r in reqs]

@router.post("", response_model=ServiceRequestResponse)
def create_service_request(
    req_in: ServiceRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    count = db.query(ServiceRequest).count() + 2001
    r_num = f"REQ-{count}"
    
    req = ServiceRequest(
        request_number=r_num,
        title=req_in.title,
        request_type=req_in.request_type,
        description=req_in.description,
        urgency=req_in.urgency,
        status=ServiceRequestStatus.SUBMITTED,
        requester_id=current_user.id,
        approval_required=True,
        sla_due=now + timedelta(hours=24),
        created_at=now
    )
    db.add(req)
    db.flush()

    db.add(Notification(
        title=f"Service Request Created: {r_num}",
        message=f"{req_in.title} submitted by {current_user.full_name}.",
        notification_type="Incident",
        severity="Info",
        link="/service-requests"
    ))

    db.add(AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="SERVICE_REQUEST_CREATED",
        resource_type="ServiceRequest",
        resource_id=r_num,
        details=f"Created service request {r_num}: {req_in.title}"
    ))

    db.commit()
    db.refresh(req)
    return req

@router.put("/{id}", response_model=ServiceRequestResponse)
def update_service_request(
    id: int,
    req_in: ServiceRequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(ServiceRequest).filter(ServiceRequest.id == id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Service request not found")
        
    if req_in.status:
        req.status = req_in.status
        if req_in.status == ServiceRequestStatus.APPROVED:
            req.approver_name = current_user.full_name
        elif req_in.status == ServiceRequestStatus.COMPLETED:
            req.completed_at = datetime.now(timezone.utc)
            
    if req_in.assigned_to:
        req.assigned_to = req_in.assigned_to
    if req_in.approval_notes:
        req.approval_notes = req_in.approval_notes
        
    req.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(req)
    return req
