export type UserRole = 'End User' | 'Service Desk Agent' | 'IT Manager' | 'Administrator' | 'SRE Lead' | 'CAB Approver' | 'Department Manager';
export type IncidentPriority = 'P1' | 'P2' | 'P3' | 'P4';
export type IncidentStatus = 'New' | 'Assigned' | 'In Progress' | 'Pending' | 'Resolved' | 'Closed';
export type ServiceRequestStatus = 'Submitted' | 'Pending Approval' | 'Approved' | 'Rejected' | 'In Progress' | 'Completed' | 'Cancelled';
export type ProblemStatus = 'Logged' | 'Under Investigation' | 'Known Error' | 'Workaround Found' | 'Resolved' | 'Closed';
export type ChangeType = 'Standard' | 'Normal' | 'Emergency';
export type ChangeStatus = 'Requested' | 'Assessment' | 'Approval' | 'Scheduled' | 'Implementation' | 'Validation' | 'Completed' | 'Rejected';
export type AssetType = 'Laptop' | 'Desktop' | 'Server' | 'Database server' | 'Router' | 'Switch' | 'Printer' | 'Cloud instance' | 'Application';
export type AssetStatus = 'Active' | 'Maintenance' | 'Decommissioned' | 'Reserved';
export type HealthStatus = 'Healthy' | 'Warning' | 'Critical';
export type AlertSeverity = 'Info' | 'Warning' | 'Critical';

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  department_id?: number;
  job_title?: string;
  department_name?: string;
}

export interface Incident {
  id: number;
  incident_number: string;
  title: string;
  description: string;
  category: string;
  impact: string;
  urgency: string;
  priority: IncidentPriority;
  status: IncidentStatus;
  reporter_id: number;
  reporter_name?: string;
  assigned_technician_id?: number;
  assigned_technician_name?: string;
  department_id?: number;
  department_name?: string;
  affected_service?: string;
  asset_id?: number;
  asset_name?: string;
  
  sla_response_due?: string;
  sla_resolution_due?: string;
  responded_at?: string;
  resolved_at?: string;
  closed_at?: string;
  sla_response_breached: boolean;
  sla_resolution_breached: boolean;
  
  ai_probable_cause?: string;
  ai_recommendations?: string;
  ai_confidence?: number;
  ai_suggested_kb_ids?: string;
  ai_similar_incidents?: string;
  
  resolution_notes?: string;
  root_cause?: string;
  
  jira_issue_key?: string;
  jira_sync_status?: string;
  jira_issue_url?: string;
  
  created_at: string;
  updated_at: string;
  comments_count?: number;
}

export interface Comment {
  id: number;
  incident_id?: number;
  service_request_id?: number;
  author_name: string;
  author_role?: string;
  content: string;
  is_internal: boolean;
  created_at: string;
}

export interface IncidentHistory {
  id: number;
  action: string;
  field_changed?: string;
  old_value?: string;
  new_value?: string;
  actor_name?: string;
  timestamp: string;
}

export interface ServiceRequest {
  id: number;
  request_number: string;
  title: string;
  request_type: string;
  description: string;
  urgency: string;
  status: ServiceRequestStatus;
  requester_id: number;
  requester_name?: string;
  assigned_to?: string;
  approval_required: boolean;
  approver_name?: string;
  approval_notes?: string;
  sla_due?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Problem {
  id: number;
  problem_number: string;
  title: string;
  description: string;
  category: string;
  status: ProblemStatus;
  impact: string;
  root_cause?: string;
  workaround?: string;
  permanent_solution?: string;
  assigned_team?: string;
  created_at: string;
  updated_at: string;
  related_incident_count: number;
  incident_numbers: string[];
}

export interface ChangeItem {
  id: number;
  change_number: string;
  title: string;
  change_type: ChangeType;
  status: ChangeStatus;
  requester_name: string;
  assigned_team?: string;
  description: string;
  reason_for_change?: string;
  risk_level: string;
  impact_level: string;
  implementation_plan: string;
  rollback_plan: string;
  test_plan?: string;
  scheduled_start?: string;
  scheduled_end?: string;
  actual_start?: string;
  actual_end?: string;
  approver_name?: string;
  approval_date?: string;
  created_at: string;
  updated_at: string;
}

export interface Asset {
  id: number;
  asset_tag: string;
  asset_name: string;
  asset_type: AssetType;
  serial_number?: string;
  owner?: string;
  department?: string;
  location?: string;
  status: AssetStatus;
  ip_address?: string;
  mac_address?: string;
  operating_system?: string;
  cpu_cores?: number;
  ram_gb?: number;
  storage_gb?: number;
  purchase_date?: string;
  warranty_expiry?: string;
  created_at: string;
  updated_at: string;
  linked_incidents_count: number;
}

export interface InfrastructureNode {
  id: number;
  hostname: string;
  node_type: string;
  ip_address: string;
  environment: string;
  status: HealthStatus;
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  network_traffic_mbps: number;
  response_time_ms: number;
  uptime_percentage: number;
  last_ping: string;
}

export interface Alert {
  id: number;
  alert_code: string;
  source: string;
  resource_name: string;
  metric_name: string;
  metric_value: number;
  threshold_value: number;
  severity: AlertSeverity;
  message: string;
  incident_created: boolean;
  incident_number?: string;
  is_acknowledged: boolean;
  created_at: string;
}

export interface KnowledgeArticle {
  id: number;
  article_number: string;
  title: string;
  category: string;
  problem_summary: string;
  symptoms: string;
  cause: string;
  resolution: string;
  tags?: string;
  views_count: number;
  helpful_count: number;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: number;
  user_id?: number;
  title: string;
  message: string;
  notification_type: string;
  severity: string;
  is_read: boolean;
  link?: string;
  created_at: string;
}

export interface AuditLog {
  id: number;
  username: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  details?: string;
  ip_address?: string;
  timestamp: string;
}

export interface AIAnalysisResult {
  suggested_category: string;
  calculated_priority: IncidentPriority;
  probable_cause: string;
  recommended_actions: string[];
  confidence_score: number;
  relevant_kb_articles: Array<{
    article_number: string;
    title: string;
    category: string;
    resolution: string;
  }>;
  similar_incidents: Array<{
    incident_number: string;
    title: string;
    priority: string;
    status: string;
  }>;
  is_anomaly_detected: boolean;
  anomaly_details?: string;
  disclaimer: string;
}

export interface DevOpsStatus {
  mode: string;
  github: {
    connected: boolean;
    mode: string;
    repository: string;
    default_branch: string;
    total_commits: number;
    open_pull_requests: number;
    latest_commit: {
      sha: string;
      message: string;
      author: string;
      timestamp: string;
      url: string;
    };
    recent_commits: Array<{
      sha: string;
      message: string;
      author: string;
      time: string;
    }>;
  };
  jira: {
    connected: boolean;
    mode: string;
    url: string;
    project: string;
    open_issues_count: number;
    recent_issues: any[];
  };
  jenkins: {
    connected: boolean;
    mode: string;
    jenkins_url: string;
    pipeline_name: string;
    latest_build: {
      number: number;
      status: string;
      duration: string;
      timestamp: string;
      triggered_by: string;
      stages: Array<{
        name: string;
        status: string;
        duration: string;
      }>;
    };
  };
  docker: {
    engine_status: string;
    containers: Array<{
      name: string;
      image: string;
      status: string;
      health: string;
      port: string;
      cpu: string;
      memory: string;
    }>;
    images_count: number;
    volumes_active: number;
  };
}
