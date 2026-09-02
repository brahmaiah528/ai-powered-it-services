from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, EmailStr
from app.models.models import (
    UserRole, IncidentPriority, IncidentStatus, ServiceRequestStatus,
    ProblemStatus, ChangeType, ChangeStatus, AssetType, AssetStatus,
    HealthStatus, AlertSeverity
)

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole = UserRole.END_USER
    department_id: Optional[int] = None
    job_title: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    department_name: Optional[str] = None

    class Config:
        from_attributes = True

# Department Schemas
class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Comment Schemas
class CommentCreate(BaseModel):
    content: str
    is_internal: bool = False

class CommentResponse(BaseModel):
    id: int
    incident_id: Optional[int] = None
    service_request_id: Optional[int] = None
    author_name: str
    author_role: Optional[str] = None
    content: str
    is_internal: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Incident History Schema
class IncidentHistoryResponse(BaseModel):
    id: int
    action: str
    field_changed: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    actor_name: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

# Incident Schemas
class IncidentCreate(BaseModel):
    title: str
    description: str
    category: Optional[str] = "Software"
    impact: str = "Medium" # High, Medium, Low
    urgency: str = "Medium" # High, Medium, Low
    affected_service: Optional[str] = None
    department_id: Optional[int] = None
    asset_id: Optional[int] = None
    assigned_technician_id: Optional[int] = None

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    impact: Optional[str] = None
    urgency: Optional[str] = None
    priority: Optional[IncidentPriority] = None
    status: Optional[IncidentStatus] = None
    assigned_technician_id: Optional[int] = None
    department_id: Optional[int] = None
    affected_service: Optional[str] = None
    asset_id: Optional[int] = None
    resolution_notes: Optional[str] = None
    root_cause: Optional[str] = None

class IncidentAssign(BaseModel):
    technician_id: int

class IncidentResolve(BaseModel):
    resolution_notes: str
    root_cause: Optional[str] = None

class IncidentResponse(BaseModel):
    id: int
    incident_number: str
    title: str
    description: str
    category: str
    impact: str
    urgency: str
    priority: IncidentPriority
    status: IncidentStatus
    reporter_id: int
    reporter_name: Optional[str] = None
    assigned_technician_id: Optional[int] = None
    assigned_technician_name: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    affected_service: Optional[str] = None
    asset_id: Optional[int] = None
    asset_name: Optional[str] = None
    
    sla_response_due: Optional[datetime] = None
    sla_resolution_due: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    sla_response_breached: bool = False
    sla_resolution_breached: bool = False
    
    ai_probable_cause: Optional[str] = None
    ai_recommendations: Optional[str] = None
    ai_confidence: Optional[float] = None
    ai_suggested_kb_ids: Optional[str] = None
    ai_similar_incidents: Optional[str] = None
    
    resolution_notes: Optional[str] = None
    root_cause: Optional[str] = None
    
    jira_issue_key: Optional[str] = None
    jira_sync_status: Optional[str] = None
    jira_issue_url: Optional[str] = None
    
    created_at: datetime
    updated_at: datetime
    comments_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Service Request Schemas
class ServiceRequestCreate(BaseModel):
    title: str
    request_type: str
    description: str
    urgency: str = "Medium"

class ServiceRequestUpdate(BaseModel):
    status: Optional[ServiceRequestStatus] = None
    assigned_to: Optional[str] = None
    approval_notes: Optional[str] = None

class ServiceRequestResponse(BaseModel):
    id: int
    request_number: str
    title: str
    request_type: str
    description: str
    urgency: str
    status: ServiceRequestStatus
    requester_id: int
    requester_name: Optional[str] = None
    assigned_to: Optional[str] = None
    approval_required: bool
    approver_name: Optional[str] = None
    approval_notes: Optional[str] = None
    sla_due: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Problem Schemas
class ProblemCreate(BaseModel):
    title: str
    description: str
    category: str
    impact: str = "High"
    assigned_team: Optional[str] = None
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    permanent_solution: Optional[str] = None
    incident_ids: Optional[List[int]] = []

class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    status: Optional[ProblemStatus] = None
    impact: Optional[str] = None
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    permanent_solution: Optional[str] = None
    assigned_team: Optional[str] = None
    incident_ids: Optional[List[int]] = None

class ProblemResponse(BaseModel):
    id: int
    problem_number: str
    title: str
    description: str
    category: str
    status: ProblemStatus
    impact: str
    root_cause: Optional[str] = None
    workaround: Optional[str] = None
    permanent_solution: Optional[str] = None
    assigned_team: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    related_incident_count: Optional[int] = 0
    incident_numbers: Optional[List[str]] = []

    class Config:
        from_attributes = True

# Change Schemas
class ChangeCreate(BaseModel):
    title: str
    change_type: ChangeType = ChangeType.NORMAL
    requester_name: str
    assigned_team: Optional[str] = None
    description: str
    reason_for_change: Optional[str] = None
    risk_level: str = "Medium"
    impact_level: str = "Medium"
    implementation_plan: str
    rollback_plan: str
    test_plan: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None

class ChangeUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[ChangeStatus] = None
    approver_name: Optional[str] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    implementation_plan: Optional[str] = None
    rollback_plan: Optional[str] = None

class ChangeResponse(BaseModel):
    id: int
    change_number: str
    title: str
    change_type: ChangeType
    status: ChangeStatus
    requester_name: str
    assigned_team: Optional[str] = None
    description: str
    reason_for_change: Optional[str] = None
    risk_level: str
    impact_level: str
    implementation_plan: str
    rollback_plan: str
    test_plan: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    approver_name: Optional[str] = None
    approval_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Asset Schemas
class AssetCreate(BaseModel):
    asset_tag: str
    asset_name: str
    asset_type: AssetType
    serial_number: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    status: AssetStatus = AssetStatus.ACTIVE
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    operating_system: Optional[str] = None
    cpu_cores: Optional[int] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    purchase_date: Optional[datetime] = None
    warranty_expiry: Optional[datetime] = None

class AssetUpdate(BaseModel):
    asset_name: Optional[str] = None
    status: Optional[AssetStatus] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    ip_address: Optional[str] = None

class AssetResponse(BaseModel):
    id: int
    asset_tag: str
    asset_name: str
    asset_type: AssetType
    serial_number: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    status: AssetStatus
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    operating_system: Optional[str] = None
    cpu_cores: Optional[int] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    purchase_date: Optional[datetime] = None
    warranty_expiry: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    linked_incidents_count: Optional[int] = 0

    class Config:
        from_attributes = True

# Infrastructure Node Schemas
class InfrastructureNodeResponse(BaseModel):
    id: int
    hostname: str
    node_type: str
    ip_address: str
    environment: str
    status: HealthStatus
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_traffic_mbps: float
    response_time_ms: float
    uptime_percentage: float
    last_ping: datetime

    class Config:
        from_attributes = True

class MetricSpikeSimulation(BaseModel):
    hostname: str
    metric: str # "CPU", "Memory", "Disk"
    value: float # e.g. 94.5

# Alert Schemas
class AlertResponse(BaseModel):
    id: int
    alert_code: str
    source: str
    resource_name: str
    metric_name: str
    metric_value: float
    threshold_value: float
    severity: AlertSeverity
    message: str
    incident_created: bool
    incident_number: Optional[str] = None
    is_acknowledged: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Knowledge Base Schemas
class KnowledgeArticleCreate(BaseModel):
    title: str
    category: str
    problem_summary: str
    symptoms: str
    cause: str
    resolution: str
    tags: Optional[str] = None

class KnowledgeArticleResponse(BaseModel):
    id: int
    article_number: str
    title: str
    category: str
    problem_summary: str
    symptoms: str
    cause: str
    resolution: str
    tags: Optional[str] = None
    views_count: int
    helpful_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Notification Schemas
class NotificationResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    title: str
    message: str
    notification_type: str
    severity: str
    is_read: bool
    link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    username: str
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[str] = None
    ip_address: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

# AI Diagnostic Schemas
class AIAnalysisRequest(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    impact: Optional[str] = "Medium"
    urgency: Optional[str] = "Medium"
    affected_service: Optional[str] = None
    error_logs: Optional[str] = None

class AIAnalysisResponse(BaseModel):
    suggested_category: str
    calculated_priority: IncidentPriority
    probable_cause: str
    recommended_actions: List[str]
    confidence_score: float
    relevant_kb_articles: List[Dict[str, Any]]
    similar_incidents: List[Dict[str, Any]]
    is_anomaly_detected: bool
    anomaly_details: Optional[str] = None
    disclaimer: str = "AI Recommendation: This analysis is an automated diagnostic recommendation generated based on historical telemetry, ITSM runbooks, and telemetry data."

# Jira Integration Schemas
class JiraCreateIssueRequest(BaseModel):
    incident_number: str
    summary: Optional[str] = None
    description: Optional[str] = None
    issue_type: str = "Bug"
    priority: str = "High"

class JiraIssueResponse(BaseModel):
    jira_key: str
    incident_number: str
    summary: str
    status: str
    priority: str
    assignee: Optional[str] = None
    url: str
    sync_status: str

# DevOps Hub Schemas
class DevOpsStatusResponse(BaseModel):
    mode: str # "Demo Mode" or "Live Integration"
    github: Dict[str, Any]
    jira: Dict[str, Any]
    jenkins: Dict[str, Any]
    docker: Dict[str, Any]
