from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.models import Asset, AssetStatus, User, AuditLog
from app.schemas.schemas import AssetCreate, AssetUpdate, AssetResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/assets", tags=["Asset Management"])

@router.get("", response_model=List[AssetResponse])
def get_assets(
    asset_type: Optional[str] = None,
    status: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Asset)
    if asset_type:
        q = q.filter(Asset.asset_type == asset_type)
    if status:
        q = q.filter(Asset.status == status)
    if department:
        q = q.filter(Asset.department == department)
    assets = q.order_by(desc(Asset.id)).all()
    
    return [AssetResponse(
        id=a.id,
        asset_tag=a.asset_tag,
        asset_name=a.asset_name,
        asset_type=a.asset_type,
        serial_number=a.serial_number,
        owner=a.owner,
        department=a.department,
        location=a.location,
        status=a.status,
        ip_address=a.ip_address,
        mac_address=a.mac_address,
        operating_system=a.operating_system,
        cpu_cores=a.cpu_cores,
        ram_gb=a.ram_gb,
        storage_gb=a.storage_gb,
        purchase_date=a.purchase_date,
        warranty_expiry=a.warranty_expiry,
        created_at=a.created_at,
        updated_at=a.updated_at,
        linked_incidents_count=len(a.incidents)
    ) for a in assets]

@router.post("", response_model=AssetResponse)
def create_asset(
    asset_in: AssetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = Asset(
        asset_tag=asset_in.asset_tag,
        asset_name=asset_in.asset_name,
        asset_type=asset_in.asset_type,
        serial_number=asset_in.serial_number,
        owner=asset_in.owner,
        department=asset_in.department,
        location=asset_in.location,
        status=asset_in.status,
        ip_address=asset_in.ip_address,
        mac_address=asset_in.mac_address,
        operating_system=asset_in.operating_system,
        cpu_cores=asset_in.cpu_cores,
        ram_gb=asset_in.ram_gb,
        storage_gb=asset_in.storage_gb,
        purchase_date=asset_in.purchase_date,
        warranty_expiry=asset_in.warranty_expiry,
        created_at=datetime.now(timezone.utc)
    )
    db.add(asset)
    db.flush()

    db.add(AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        action="ASSET_CREATED",
        resource_type="Asset",
        resource_id=asset.asset_tag,
        details=f"Created asset {asset.asset_tag}: {asset.asset_name}"
    ))

    db.commit()
    db.refresh(asset)
    return asset

@router.put("/{id}", response_model=AssetResponse)
def update_asset(
    id: int,
    asset_in: AssetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    asset = db.query(Asset).filter(Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    if asset_in.asset_name:
        asset.asset_name = asset_in.asset_name
    if asset_in.status:
        asset.status = asset_in.status
    if asset_in.owner:
        asset.owner = asset_in.owner
    if asset_in.department:
        asset.department = asset_in.department
    if asset_in.location:
        asset.location = asset_in.location
    if asset_in.ip_address:
        asset.ip_address = asset_in.ip_address
        
    asset.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(asset)
    return asset
