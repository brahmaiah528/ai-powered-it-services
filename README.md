# AI-Powered IT Service Management and Incident Resolution Platform

An enterprise-grade **IT Operations / IT Service Management (ITSM)** platform designed to unify incident management, service requests, root-cause problem investigation, change control (RFC), IT asset CMDB, real-time infrastructure telemetry, and AI-assisted diagnostics with an end-to-end **DevOps ecosystem integrating Jira, GitHub, Jenkins, and Docker**.

---

## 🌟 Executive Summary & Key Highlights

* **Cognitive AI Incident Assistant**: Real-time domain classification (10 categories), dynamic priority matrix calculation ($\text{Priority} = \text{Impact} \times \text{Urgency}$), root cause diagnosis, and automated runbook generation with confidence scoring.
* **Full ITIL v4 Lifecycle**: Complete workflows for Incidents (New &rarr; Assigned &rarr; In Progress &rarr; Pending &rarr; Resolved &rarr; Closed), Service Requests, Problems, Changes (CAB approval & rollback plans), and Assets (CMDB).
* **Automated Infrastructure Telemetry**: Real-time monitoring of CPU, Memory, Disk, Network throughput, and Latency across database clusters, Kubernetes workers, and API gateways. Automated metric spike detection (&gt;90%) triggers alerts and auto-logs P1 critical incidents.
* **DevOps Ecosystem Orchestration**:
  * **Jira Cloud Two-Way Sync**: Automatically generates linked Jira tickets for high-priority incidents and keeps assignees and statuses in sync.
  * **GitHub Workflows**: Commits and pull requests automatically trigger CI/CD webhooks.
  * **Jenkins 11-Stage Pipeline**: Automated checkout, testing, building, Docker container packaging, zero-downtime deployment, and health checks.
  * **Docker Containerization**: Multi-stage production container images orchestrated via `docker-compose.yml`.
* **Interactive Critical Scenario Runner**: An interactive visual runner executing the complete **23-Step Critical Database Failure (INC-1025)** lifecycle from telemetry spike to automated Jira ticket, Jenkins build, and recovery.

---

## 🏗️ Architecture & Technology Stack

```
                         ENTERPRISE USERS & ENGINEERS
                                       │
                                       ▼
                    ┌──────────────────────────────────────┐
                    │      React 18 + TypeScript + Vite    │
                    │       Tailwind CSS + Lucide Icons    │
                    │      ITSM & DevOps Dashboard         │
                    └──────────────────┬───────────────────┘
                                       │ REST API / JWT
                                       ▼
                    ┌──────────────────────────────────────┐
                    │           FastAPI Backend            │
                    ├──────────────────────────────────────┤
                    │ • Incident Management (ITIL v4)      │
                    │ • Service Request Catalog            │
                    │ • Problem Management & RCA           │
                    │ • Change Management (CAB Review)     │
                    │ • CMDB & Asset Management            │
                    │ • Infrastructure Telemetry & Alerts  │
                    │ • SLA Tracking & Countdown Engine    │
                    │ • Notification & Audit Subsystems    │
                    └───────────┬──────────────┬───────────┘
                                │              │
                ┌───────────────┘              └───────────────┐
                ▼                                              ▼
    ┌───────────────────────┐                      ┌───────────────────────┐
    │   PostgreSQL Engine   │                      │  AI Diagnostic Engine │
    │    SQLAlchemy 2.0     │                      │ • Auto Classification │
    │ 16 Relational Tables  │                      │ • Priority Matrix     │
    │  History & Audit Log  │                      │ • Root Cause Analysis │
    └───────────────────────┘                      │ • Runbook Generation  │
                                                   └───────────────────────┘

                             DEVOPS ECOSYSTEM

               ┌───────────────┐               ┌───────────────┐
               │  Jira Cloud   │               │ GitHub Repo   │
               │ Two-Way Sync  │               │ Code & PRs    │
               └───────┬───────┘               └───────┬───────┘
                       │                               │
                       │                               ▼
                       │                       ┌───────────────┐
                       │                       │  Jenkins CI   │
                       │                       │ 11-Stage Pipe │
                       │                       └───────┬───────┘
                       │                               │
                       │                               ▼
                       │                       ┌───────────────┐
                       └──────────────────────►│    Docker     │
                                               │ Microservices │
                                               └───────────────┘
```

### Technology Breakdown:
* **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React Icons.
* **Backend**: Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.0, Python-Jose (JWT), Passlib (Bcrypt).
* **Database**: PostgreSQL 16 (Primary) / SQLite (Zero-config local fallback).
* **CI/CD & DevOps**: Jenkinsfile (11 stages), Docker Compose, Jira REST API, GitHub Webhooks.

---

## 🚀 Quick Start Guide

### Option 1: Running Locally with Python & Node.js

#### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create & activate Python virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server (Database automatically seeds with 30 incidents, 20 assets, 10 infra nodes, users, etc.)
uvicorn app.main:app --reload --port 8000
```
* Backend API & Swagger Docs will be live at: `http://localhost:8000/docs`

#### 2. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
* Access the Web Platform at: `http://localhost:5173`

---

### Option 2: Running with Docker Compose

Run the complete 3-tier production stack (PostgreSQL + FastAPI + React Nginx) in a single command:

```bash
docker compose up --build -d
```

* **Frontend Dashboard**: `http://localhost` (or `http://localhost:3000`)
* **Backend REST API & Swagger UI**: `http://localhost:8000/docs`
* **PostgreSQL Database**: `localhost:5432`

---

## 👥 Default Demo Credentials & RBAC Roles

The system comes pre-seeded with 10 enterprise users across 4 role tiers (all users share the password: `admin123`):

| Role | Username | Full Name | Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | Marcus Vance | Full access: user management, integrations, audit logs, and settings |
| **IT Manager** | `itmanager` | Elena Rostova | SLA monitoring, CAB change approvals, operational reports |
| **Service Desk Agent** | `srelead` | Sarah Connor | Triage, AI assistant, incident assignment, Jira sync, and resolution |
| **End User** | `user1` | Alex Morgan | Raise incidents, submit service requests, track own tickets |

*(You can also seamlessly switch roles live using the role selector in the bottom left of the application sidebar).*

---

## 🎯 23-Step End-to-End Critical Scenario Demonstration

The platform includes a dedicated **Live Scenario Runner** simulating a critical production database failure and its automated DevOps resolution:

```
[1. Telemetry Detects Spike]  Database-01 CPU exceeds 90% (Current: 94.2%)
          ↓
[2. Automated Alert]          System logs critical alert ALT-94201
          ↓
[3. Incident Creation]        P1 Incident INC-1025 automatically created
          ↓
[4. Prioritization]           High Impact x High Urgency = P1 Critical (15m Response, 2h Resolution SLA)
          ↓
[5. AI Analysis]              AI Diagnostic Engine evaluates telemetry and query patterns
          ↓
[6. Probable Cause]           Identifies lock contention & unindexed queries (96.5% confidence)
          ↓
[7. Runbook Actions]          Recommends killing blocking PIDs, creating index, scaling connection pool
          ↓
[8. Notification]             Broadcast alert sent to On-Call SRE and DB Administrators
          ↓
[9. CMDB Mapping]             Incident linked to Asset AST-5001 (PostgreSQL Primary Cluster)
          ↓
[10. Jira Integration]        Jira ticket ITSM-245 automatically created
          ↓
[11. SRE Assignment]          Assigned to Sarah Connor (Senior Database SRE) in Jira
          ↓
[12. Triage & Hotfix]         Engineer terminates deadlocks and authors optimization patch
          ↓
[13. GitHub Commit]           Pushes commit e9a1b42 to main branch
          ↓
[14. Jenkins Webhook]         GitHub triggers Jenkins CI/CD pipeline
          ↓
[15. Automated Tests]         Jenkins executes pytest backend & frontend build verification
          ↓
[16. Docker Build]            Jenkins builds itsm-backend:e9a1b42 container image
          ↓
[17. Container Deployment]    Zero-downtime container rollout deployed
          ↓
[18. Health Verification]     Infrastructure telemetry verifies CPU drops from 94.2% down to 28.4% (Healthy)
          ↓
[19. Incident Resolution]     INC-1025 status transitions to Resolved
          ↓
[20. Runbook Capture]         Resolution notes and SQL migration recorded in incident audit history
          ↓
[21. Jira Sync]               Jira ticket ITSM-245 automatically updated to 'Done'
          ↓
[22. SLA Metrics]             Resolved in 32 minutes (SLA Met without breach)
          ↓
[23. Executive Dashboard]     Command center KPIs, MTTR, and active alert counters update in real time
```

---

## 🧪 Testing Instructions

Run the automated backend test suite covering authentication, incident workflows, SLA matrix calculations, AI diagnostics, and Jira synchronization:

```bash
# Run backend tests
pytest tests/backend/ -v
```

---

## 📁 Repository Directory Structure

```
it-service-management/
├── backend/
│   ├── app/
│   │   ├── api/             # REST API routers (Incidents, AI, Jira, DevOps, etc.)
│   │   ├── core/            # Config, database engine, security JWT, seed data
│   │   ├── models/          # SQLAlchemy relational entities
│   │   ├── schemas/         # Pydantic v2 schemas
│   │   ├── services/        # AI engine, Jira sync, DevOps, SLA services
│   │   └── main.py          # FastAPI application entrypoint
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/      # Sidebar, Topbar, Modals, AI drawer, Scenario runner
│   │   ├── context/         # AuthContext, NotificationContext
│   │   ├── pages/           # Dashboard, Incidents, AI Hub, DevOps, Assets, etc.
│   │   ├── services/        # API client
│   │   ├── types/           # TypeScript interfaces
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── nginx.conf
├── database/
│   └── schema.sql           # PostgreSQL DDL
├── tests/
│   └── backend/             # Pytest automated test suite
├── docs/                    # Architecture, Demo scenario, API reference
├── docker-compose.yml       # 3-tier container orchestration
├── Jenkinsfile              # 11-stage CI/CD pipeline
├── README.md
└── .gitignore
```
