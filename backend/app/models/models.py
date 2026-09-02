import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum as SQLEnum, Table
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class UserRole(str, enum.Enum):
    END_USER = "End User"
    SERVICE_DESK_AGENT = "Service Desk Agent"
    IT_MANAGER = "IT Manager"
    ADMINISTRATOR = "Administrator"

class IncidentPriority(str, enum.Enum):
    P1 = "P1"  # Critical
    P2 = "P2"  # High
    P3 = "P3"  # Medium
    P4 = "P4"  # Low

class IncidentStatus(str, enum.Enum):
    NEW = "New"
    ASSIGNED = "Assigned"
    IN_PROGRESS = "In Progress"
    PENDING = "Pending"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class ServiceRequestStatus(str, enum.Enum):
    SUBMITTED = "Submitted"
    PENDING_APPROVAL = "Pending Approval"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class ProblemStatus(str, enum.Enum):
    LOGGED = "Logged"
    UNDER_INVESTIGATION = "Under Investigation"
    KNOWN_ERROR = "Known Error"
    WORKAROUND_FOUND = "Workaround Found"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class ChangeType(str, enum.Enum):
    STANDARD = "Standard"
    NORMAL = "Normal"
    EMERGENCY = "Emergency"

class ChangeStatus(str, enum.Enum):
    REQUESTED = "Requested"
    ASSESSMENT = "Assessment"
    APPROVAL = "Approval"
    SCHEDULED = "Scheduled"
    IMPLEMENTATION = "Implementation"
    VALIDATION = "Validation"
    COMPLETED = "Completed"
    REJECTED = "Rejected"

class AssetType(str, enum.Enum):
    LAPTOP = "Laptop"
    DESKTOP = "Desktop"
    SERVER = "Server"
    DATABASE_SERVER = "Database server"
    ROUTER = "Router"
    SWITCH = "Switch"
    PRINTER = "Printer"
    CLOUD_INSTANCE = "Cloud instance"
    APPLICATION = "Application"

class AssetStatus(str, enum.Enum):
    ACTIVE = "Active"
    MAINTENANCE = "Maintenance"
    DECOMMISSIONED = "Decommissioned"
    RESERVED = "Reserved"

class HealthStatus(str, enum.Enum):
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"

class AlertSeverity(str, enum.Enum):
    INFO = "Info"
    WARNING = "Warning"
    CRITICAL = "Critical"

# Association table for Problems and Incidents
problem_incidents = Table(
    "problem_incidents",
    Base.metadata,
    Column("problem_id", Integer, ForeignKey("problems.id"), primary_key=True),
    Column("incident_id", Integer, ForeignKey("incidents.id"), primary_key=True),
)

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    users = relationship("User", back_populates="department")
    incidents = relationship("Incident", back_populates="department")

class BusinessUnit(Base):
    __tablename__ = "business_units"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(20), nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    username = Column(String(60), unique=True, index=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.END_USER, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    job_title = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    department = relationship("Department", back_populates="users")
    reported_incidents = relationship("Incident", foreign_keys="[Incident.reporter_id]", back_populates="reporter")
    assigned_incidents = relationship("Incident", foreign_keys="[Incident.assigned_technician_id]", back_populates="assigned_technician")
    service_requests = relationship("ServiceRequest", back_populates="requester")
    audit_logs = relationship("AuditLog", back_populates="user")

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    incident_number = Column(String(30), unique=True, index=True, nullable=False) # e.g. INC-1001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default="Software") # Network, Hardware, Software, Database, Security, Cloud, Email, Authentication, Application, Infrastructure
    impact = Column(String(20), default="Medium") # High, Medium, Low
    urgency = Column(String(20), default="Medium") # High, Medium, Low
    priority = Column(SQLEnum(IncidentPriority), default=IncidentPriority.P3, nullable=False)
    status = Column(SQLEnum(IncidentStatus), default=IncidentStatus.NEW, nullable=False)
    
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    affected_service = Column(String(100), nullable=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    
    # SLA Tracking
    sla_response_due = Column(DateTime, nullable=True)
    sla_resolution_due = Column(DateTime, nullable=True)
    responded_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    sla_response_breached = Column(Boolean, default=False)
    sla_resolution_breached = Column(Boolean, default=False)
    
    # AI Resolution Recommendation Details
    ai_probable_cause = Column(Text, nullable=True)
    ai_recommendations = Column(Text, nullable=True)
    ai_confidence = Column(Float, nullable=True) # 0.0 - 100.0
    ai_suggested_kb_ids = Column(String(255), nullable=True) # Comma separated
    ai_similar_incidents = Column(String(255), nullable=True) # e.g. "INC-1001, INC-1005"
    
    # Resolution Notes
    resolution_notes = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    
    # Jira Synchronization
    jira_issue_key = Column(String(50), nullable=True) # e.g. JIRA-245
    jira_sync_status = Column(String(50), default="Not Linked") # Linked, In Sync, Pending Sync
    jira_issue_url = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reported_incidents")
    assigned_technician = relationship("User", foreign_keys=[assigned_technician_id], back_populates="assigned_incidents")
    department = relationship("Department", back_populates="incidents")
    asset = relationship("Asset", back_populates="incidents")
    comments = relationship("Comment", back_populates="incident", cascade="all, delete-orphan")
    history = relationship("IncidentHistory", back_populates="incident", cascade="all, delete-orphan")
    problems = relationship("Problem", secondary=problem_incidents, back_populates="incidents")

class IncidentHistory(Base):
    __tablename__ = "incident_history"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    action = Column(String(100), nullable=False)
    field_changed = Column(String(50), nullable=True)
    old_value = Column(String(255), nullable=True)
    new_value = Column(String(255), nullable=True)
    actor_name = Column(String(120), nullable=True)
    timestamp = Column(DateTime, default=utc_now)

    incident = relationship("Incident", back_populates="history")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    service_request_id = Column(Integer, ForeignKey("service_requests.id"), nullable=True)
    author_name = Column(String(120), nullable=False)
    author_role = Column(String(60), nullable=True)
    content = Column(Text, nullable=False)
    is_internal = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

    incident = relationship("Incident", back_populates="comments")
    service_request = relationship("ServiceRequest", back_populates="comments")

class ServiceRequest(Base):
    __tablename__ = "service_requests"
    id = Column(Integer, primary_key=True, index=True)
    request_number = Column(String(30), unique=True, index=True, nullable=False) # e.g. REQ-2001
    title = Column(String(255), nullable=False)
    request_type = Column(String(100), nullable=False) # Password reset, VPN access, Hardware request, Software installation, etc.
    description = Column(Text, nullable=False)
    urgency = Column(String(20), default="Medium")
    status = Column(SQLEnum(ServiceRequestStatus), default=ServiceRequestStatus.SUBMITTED, nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(String(120), nullable=True)
    approval_required = Column(Boolean, default=True)
    approver_name = Column(String(120), nullable=True)
    approval_notes = Column(Text, nullable=True)
    sla_due = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    requester = relationship("User", back_populates="service_requests")
    comments = relationship("Comment", back_populates="service_request", cascade="all, delete-orphan")

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    problem_number = Column(String(30), unique=True, index=True, nullable=False) # e.g. PRB-3001
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    status = Column(SQLEnum(ProblemStatus), default=ProblemStatus.LOGGED, nullable=False)
    impact = Column(String(20), default="High")
    root_cause = Column(Text, nullable=True)
    workaround = Column(Text, nullable=True)
    permanent_solution = Column(Text, nullable=True)
    assigned_team = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    incidents = relationship("Incident", secondary=problem_incidents, back_populates="problems")

class Change(Base):
    __tablename__ = "changes"
    id = Column(Integer, primary_key=True, index=True)
    change_number = Column(String(30), unique=True, index=True, nullable=False) # e.g. CHG-4001
    title = Column(String(255), nullable=False)
    change_type = Column(SQLEnum(ChangeType), default=ChangeType.NORMAL, nullable=False)
    status = Column(SQLEnum(ChangeStatus), default=ChangeStatus.REQUESTED, nullable=False)
    requester_name = Column(String(120), nullable=False)
    assigned_team = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    reason_for_change = Column(Text, nullable=True)
    risk_level = Column(String(20), default="Medium") # Low, Medium, High, Critical
    impact_level = Column(String(20), default="Medium")
    implementation_plan = Column(Text, nullable=False)
    rollback_plan = Column(Text, nullable=False)
    test_plan = Column(Text, nullable=True)
    scheduled_start = Column(DateTime, nullable=True)
    scheduled_end = Column(DateTime, nullable=True)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    approver_name = Column(String(120), nullable=True)
    approval_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String(50), unique=True, index=True, nullable=False) # e.g. AST-5001
    asset_name = Column(String(150), nullable=False)
    asset_type = Column(SQLEnum(AssetType), nullable=False)
    serial_number = Column(String(100), nullable=True)
    owner = Column(String(120), nullable=True)
    department = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    status = Column(SQLEnum(AssetStatus), default=AssetStatus.ACTIVE, nullable=False)
    ip_address = Column(String(50), nullable=True)
    mac_address = Column(String(50), nullable=True)
    operating_system = Column(String(100), nullable=True)
    cpu_cores = Column(Integer, nullable=True)
    ram_gb = Column(Integer, nullable=True)
    storage_gb = Column(Integer, nullable=True)
    purchase_date = Column(DateTime, nullable=True)
    warranty_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    incidents = relationship("Incident", back_populates="asset")

class InfrastructureNode(Base):
    __tablename__ = "infrastructure_nodes"
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(100), unique=True, index=True, nullable=False) # e.g. db-prod-primary-01
    node_type = Column(String(50), nullable=False) # Database, Web Server, App Server, Kubernetes Worker, API Gateway, Load Balancer
    ip_address = Column(String(50), nullable=False)
    environment = Column(String(30), default="Production") # Production, Staging, Development
    status = Column(SQLEnum(HealthStatus), default=HealthStatus.HEALTHY, nullable=False)
    
    cpu_usage = Column(Float, default=24.5) # %
    memory_usage = Column(Float, default=45.2) # %
    disk_usage = Column(Float, default=58.0) # %
    network_traffic_mbps = Column(Float, default=120.4)
    response_time_ms = Column(Float, default=18.5)
    uptime_percentage = Column(Float, default=99.98)
    
    last_ping = Column(DateTime, default=utc_now)
    created_at = Column(DateTime, default=utc_now)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    alert_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. ALT-9001
    source = Column(String(100), nullable=False) # Infrastructure, Application, Network, Security
    resource_name = Column(String(100), nullable=False) # e.g. Database-01
    metric_name = Column(String(50), nullable=False) # CPU, Memory, Disk, Response Time
    metric_value = Column(Float, nullable=False)
    threshold_value = Column(Float, nullable=False)
    severity = Column(SQLEnum(AlertSeverity), default=AlertSeverity.WARNING, nullable=False)
    message = Column(Text, nullable=False)
    incident_created = Column(Boolean, default=False)
    incident_number = Column(String(30), nullable=True)
    is_acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"
    id = Column(Integer, primary_key=True, index=True)
    article_number = Column(String(30), unique=True, index=True, nullable=False) # e.g. KB-101
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    problem_summary = Column(Text, nullable=False)
    symptoms = Column(Text, nullable=False)
    cause = Column(Text, nullable=False)
    resolution = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True) # Comma separated
    views_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Null = global broadcast
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="Incident") # Incident, SLA, Change, Alert, System, DevOps
    severity = Column(String(20), default="Info") # Info, Warning, Error, Success
    is_read = Column(Boolean, default=False)
    link = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    username = Column(String(120), nullable=False)
    action = Column(String(100), nullable=False) # e.g. "USER_LOGIN", "INCIDENT_CREATED", "JIRA_SYNC", "CHANGE_APPROVED"
    resource_type = Column(String(50), nullable=False) # Incident, User, Asset, Change, DevOps
    resource_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="audit_logs")

class SLAPolicy(Base):
    __tablename__ = "sla_policies"
    id = Column(Integer, primary_key=True, index=True)
    priority = Column(SQLEnum(IncidentPriority), unique=True, nullable=False)
    response_time_minutes = Column(Integer, nullable=False) # e.g. P1: 15m, P2: 30m, P3: 120m, P4: 480m
    resolution_time_minutes = Column(Integer, nullable=False) # e.g. P1: 120m, P2: 240m, P3: 480m, P4: 1440m
    description = Column(String(255), nullable=True)

class JiraIssueLink(Base):
    __tablename__ = "jira_links"
    id = Column(Integer, primary_key=True, index=True)
    incident_number = Column(String(30), unique=True, index=True, nullable=False)
    jira_key = Column(String(50), unique=True, index=True, nullable=False) # e.g. ITSM-245
    jira_summary = Column(String(255), nullable=False)
    jira_status = Column(String(50), default="To Do")
    jira_priority = Column(String(30), default="High")
    jira_assignee = Column(String(100), nullable=True)
    last_synced = Column(DateTime, default=utc_now)
    created_at = Column(DateTime, default=utc_now)
