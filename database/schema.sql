-- PostgreSQL Database Schema for AI-Powered IT Service Management Platform
-- Database: itsm_db

CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS business_units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    username VARCHAR(60) UNIQUE NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'End User',
    department_id INTEGER REFERENCES departments(id),
    job_title VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    asset_tag VARCHAR(50) UNIQUE NOT NULL,
    asset_name VARCHAR(150) NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    serial_number VARCHAR(100),
    owner VARCHAR(120),
    department VARCHAR(100),
    location VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    ip_address VARCHAR(50),
    mac_address VARCHAR(50),
    operating_system VARCHAR(100),
    cpu_cores INTEGER,
    ram_gb INTEGER,
    storage_gb INTEGER,
    purchase_date TIMESTAMP WITH TIME ZONE,
    warranty_expiry TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    incident_number VARCHAR(30) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'Software',
    impact VARCHAR(20) DEFAULT 'Medium',
    urgency VARCHAR(20) DEFAULT 'Medium',
    priority VARCHAR(10) NOT NULL DEFAULT 'P3',
    status VARCHAR(30) NOT NULL DEFAULT 'New',
    reporter_id INTEGER NOT NULL REFERENCES users(id),
    assigned_technician_id INTEGER REFERENCES users(id),
    department_id INTEGER REFERENCES departments(id),
    affected_service VARCHAR(100),
    asset_id INTEGER REFERENCES assets(id),
    sla_response_due TIMESTAMP WITH TIME ZONE,
    sla_resolution_due TIMESTAMP WITH TIME ZONE,
    responded_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    closed_at TIMESTAMP WITH TIME ZONE,
    sla_response_breached BOOLEAN DEFAULT FALSE,
    sla_resolution_breached BOOLEAN DEFAULT FALSE,
    ai_probable_cause TEXT,
    ai_recommendations TEXT,
    ai_confidence FLOAT,
    ai_suggested_kb_ids VARCHAR(255),
    ai_similar_incidents VARCHAR(255),
    resolution_notes TEXT,
    root_cause TEXT,
    jira_issue_key VARCHAR(50),
    jira_sync_status VARCHAR(50) DEFAULT 'Not Linked',
    jira_issue_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS incident_history (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    field_changed VARCHAR(50),
    old_value VARCHAR(255),
    new_value VARCHAR(255),
    actor_name VARCHAR(120),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id) ON DELETE CASCADE,
    service_request_id INTEGER,
    author_name VARCHAR(120) NOT NULL,
    author_role VARCHAR(60),
    content TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS service_requests (
    id SERIAL PRIMARY KEY,
    request_number VARCHAR(30) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    request_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    urgency VARCHAR(20) DEFAULT 'Medium',
    status VARCHAR(30) NOT NULL DEFAULT 'Submitted',
    requester_id INTEGER NOT NULL REFERENCES users(id),
    assigned_to VARCHAR(120),
    approval_required BOOLEAN DEFAULT TRUE,
    approver_name VARCHAR(120),
    approval_notes TEXT,
    sla_due TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS problems (
    id SERIAL PRIMARY KEY,
    problem_number VARCHAR(30) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Logged',
    impact VARCHAR(20) DEFAULT 'High',
    root_cause TEXT,
    workaround TEXT,
    permanent_solution TEXT,
    assigned_team VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS problem_incidents (
    problem_id INTEGER NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    PRIMARY KEY (problem_id, incident_id)
);

CREATE TABLE IF NOT EXISTS changes (
    id SERIAL PRIMARY KEY,
    change_number VARCHAR(30) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    change_type VARCHAR(30) NOT NULL DEFAULT 'Normal',
    status VARCHAR(30) NOT NULL DEFAULT 'Requested',
    requester_name VARCHAR(120) NOT NULL,
    assigned_team VARCHAR(100),
    description TEXT NOT NULL,
    reason_for_change TEXT,
    risk_level VARCHAR(20) DEFAULT 'Medium',
    impact_level VARCHAR(20) DEFAULT 'Medium',
    implementation_plan TEXT NOT NULL,
    rollback_plan TEXT NOT NULL,
    test_plan TEXT,
    scheduled_start TIMESTAMP WITH TIME ZONE,
    scheduled_end TIMESTAMP WITH TIME ZONE,
    actual_start TIMESTAMP WITH TIME ZONE,
    actual_end TIMESTAMP WITH TIME ZONE,
    approver_name VARCHAR(120),
    approval_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS infrastructure_nodes (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(100) UNIQUE NOT NULL,
    node_type VARCHAR(50) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    environment VARCHAR(30) DEFAULT 'Production',
    status VARCHAR(30) NOT NULL DEFAULT 'Healthy',
    cpu_usage FLOAT DEFAULT 25.0,
    memory_usage FLOAT DEFAULT 45.0,
    disk_usage FLOAT DEFAULT 55.0,
    network_traffic_mbps FLOAT DEFAULT 100.0,
    response_time_ms FLOAT DEFAULT 15.0,
    uptime_percentage FLOAT DEFAULT 99.98,
    last_ping TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    alert_code VARCHAR(50) UNIQUE NOT NULL,
    source VARCHAR(100) NOT NULL,
    resource_name VARCHAR(100) NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    metric_value FLOAT NOT NULL,
    threshold_value FLOAT NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'Warning',
    message TEXT NOT NULL,
    incident_created BOOLEAN DEFAULT FALSE,
    incident_number VARCHAR(30),
    is_acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS knowledge_articles (
    id SERIAL PRIMARY KEY,
    article_number VARCHAR(30) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    problem_summary TEXT NOT NULL,
    symptoms TEXT NOT NULL,
    cause TEXT NOT NULL,
    resolution TEXT NOT NULL,
    tags VARCHAR(255),
    views_count INTEGER DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'Incident',
    severity VARCHAR(20) DEFAULT 'Info',
    is_read BOOLEAN DEFAULT FALSE,
    link VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    username VARCHAR(120) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(50),
    details TEXT,
    ip_address VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sla_policies (
    id SERIAL PRIMARY KEY,
    priority VARCHAR(10) UNIQUE NOT NULL,
    response_time_minutes INTEGER NOT NULL,
    resolution_time_minutes INTEGER NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS jira_links (
    id SERIAL PRIMARY KEY,
    incident_number VARCHAR(30) UNIQUE NOT NULL,
    jira_key VARCHAR(50) UNIQUE NOT NULL,
    jira_summary VARCHAR(255) NOT NULL,
    jira_status VARCHAR(50) DEFAULT 'To Do',
    jira_priority VARCHAR(30) DEFAULT 'High',
    jira_assignee VARCHAR(100),
    last_synced TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
