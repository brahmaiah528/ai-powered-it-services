# System Architecture: AI-Powered IT Service Management & Incident Resolution Platform

## 1. High-Level Architecture Overview

```
                         ENTERPRISE USERS & ENGINEERS
                                       │
                                       ▼
                    ┌──────────────────────────────────────┐
                    │       React 18 + TypeScript          │
                    │        Vite + Tailwind CSS           │
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
                    │ • Infrastructure Monitoring & Alerts │
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
    └───────────────────────┘                      │ • Knowledge Matching  │
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

## 2. Core Subsystems

### A. AI Diagnostic Engine
- **Classification**: Analyzes incoming incident titles, descriptions, and telemetry metrics to classify into 10 IT operational domains.
- **Priority Calculation**: Enforces the ITIL formula $\text{Priority} = \text{Impact} \times \text{Urgency}$.
- **Resolution Recommendation**: Generates step-by-step diagnostic checklists with confidence scores and references to relevant KB runbooks.

### B. SLA Engine
- Computes response and resolution deadlines dynamically on ticket creation ($P1$: 15m/2h, $P2$: 30m/4h, $P3$: 2h/8h, $P4$: 8h/24h).
- Continuously assesses breach states and updates compliance percentages in real-time.

### C. DevOps Hub
- **Jira**: Creates linked work items for high-priority incidents and keeps status/assignee synchronized.
- **GitHub**: Tracks repository commit history, pull requests, and webhooks.
- **Jenkins**: Simulates an 11-stage automated CI/CD pipeline triggered by commits.
- **Docker**: Provides live container health status for frontend, backend, and database services.
