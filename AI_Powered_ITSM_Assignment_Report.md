# SIMATS ENGINEERING • DEPARTMENT OF CSE (ARTIFICIAL INTELLIGENCE)
## CSA1011 – SOFTWARE ENGINEERING COURSEWORK
### AI-Powered IT Service Management & Incident Resolution Platform
#### Autonomous Incident Triage, Telemetry-Driven RCA, and DevOps Orchestration

**Source Repository:** [https://github.com/brahmaiah528/ai-powered-it-services](https://github.com/brahmaiah528/ai-powered-it-services)

---

## A. Assignment Information

| Metadata Field | Academic Specification |
| :--- | :--- |
| **Department** | Computer Science and Engineering in Artificial Intelligence |
| **Programme** | Bachelor of Technology in SIMATS Engineering |
| **Course Code & Title** | CSA1011 – Software Engineering |
| **Academic Year / Cohort** | 2023 |
| **Faculty Evaluator** | Dr. Ramireddy Navatejareddy |
| **Project Title** | AI-Powered IT Service Management & Incident Resolution Platform |
| **Date of Assignment Issue** | 01-09-2026 |
| **Date of Project Submission** | 02-09-2026 |
| **Total Evaluation Weightage** | 100 Marks |
| **Course Outcome & Taxonomy** | CO-6 (Bloom's Level L6: Create) \| SDG 9: Industry, Innovation & Infrastructure |
| **Industrial / Societal Relevance** | Enterprise IT Operations / SRE automation — directly applicable to site reliability engineering, modern IT service management desks, and DevOps continuous delivery. |

---

## Team Member Roles & Responsibility Matrix

| S.No. | Name | Registration No. | Role / Module Ownership |
| :---: | :--- | :---: | :--- |
| **1** | **Pramith Maredukonda** | **192372174** | **Team Lead** — FastAPI REST architecture, PostgreSQL relational schemas, Cognitive AI Diagnostic Engine, Jira 2-way sync service, and system documentation. |
| **2** | **Thonduru Sushma** | **192325135** | **Frontend Architecture** — Executive Command Dashboard, Incident Queue & Detail views, Service Request Catalog, and Change Advisory Board (CAB) review workflows. |
| **3** | **Chimaladinne Naga Anjali** | **192372201** | **DevOps & Infrastructure** — Multi-stage Docker containerization, 11-stage Jenkins CI/CD pipeline, Git Flow configuration, and Pytest automated testing suite. |
| **4** | **SRIRAM SASIDHAR SAI** | **192311276** | **Telemetry & AI Operations** — Real-time infrastructure health monitor, live metric spike fault simulation, and conversational AI Runbook Diagnostic Assistant. |

---

## Table of Contents

1. [Executive Problem Formulation and Contextual Domain Analysis](#1-executive-problem-formulation-and-contextual-domain-analysis)
2. [Scope, Engineering Objectives, and Measurable Deliverables](#2-scope-engineering-objectives-and-measurable-deliverables)
3. [Multi-Tier Requirements Specification, Constraints, and System Assumptions](#3-multi-tier-requirements-specification-constraints-and-system-assumptions)
4. [Rigorous Integration of Core Software Engineering Principles (CSA1011)](#4-rigorous-integration-of-core-software-engineering-principles-csa1011)
5. [System Architecture, Layered Decomposition, and Directory Schemas](#5-system-architecture-layered-decomposition-and-directory-schemas)
6. [Cognitive Heuristic Algorithms, Priority Formulations, and Decision Flowcharts](#6-cognitive-heuristic-algorithms-priority-formulations-and-decision-flowcharts)
7. [Technical Implementation Stack, Version Control, and Deployment Topology](#7-technical-implementation-stack-version-control-and-deployment-topology)
8. [Verification Test Matrix, Executed Assertions, and Empirical Results](#8-verification-test-matrix-executed-assertions-and-empirical-results)
9. [User Interface Walkthrough and Operational Viewports](#9-user-interface-walkthrough-and-operational-viewports)
10. [Empirical Validation, Build Verification, and Requirement Traceability](#10-empirical-validation-build-verification-and-requirement-traceability)
11. [Engineering Trade-offs, Architectural Comparison, and Design Justification](#11-engineering-trade-offs-architectural-comparison-and-design-justification)
12. [Societal Imperatives, Sustainable Compute, and UN SDG 9 Alignment](#12-societal-imperatives-sustainable-compute-and-un-sdg-9-alignment)
13. [Concluding Remarks, Architectural Constraints, and Future Roadmap](#13-concluding-remarks-architectural-constraints-and-future-roadmap)
14. [Individual Contributions and Team Responsibility Breakdown](#14-individual-contributions-and-team-responsibility-breakdown)
15. [Academic and Industry Scholarly References](#15-academic-and-industry-scholarly-references)
16. [Individual Engineering Reflections and Retrospective](#16-individual-engineering-reflections-and-retrospective)
17. [Appendix: Assessment Rubric and Course Outcome Attainment Matrix](#appendix-assessment-rubric-and-course-outcome-attainment-matrix)

---

## 1. Executive Problem Formulation and Contextual Domain Analysis

### 1.1 Problem Statement
Contemporary enterprise IT operations centers (NOCs/SOCs) face an escalating deluge of unstructured service desk tickets, continuous infrastructure telemetry feeds, and regulatory change requests. Legacy IT Service Management (ITSM) systems depend heavily on human triage operators to manually review tickets, assign severity ratings, and infer underlying failure mechanisms. This manual paradigm creates critical systemic vulnerabilities: critical P1 infrastructure outages suffer significant acknowledgement delays, ticket categorization remains inconsistent across shifts, and Mean Time to Resolution (MTTR) is severely inflated by repetitive manual diagnosis. The core engineering objective of this project is to architect, develop, containerize, and validate an intelligent, unified IT Operations platform capable of autonomous ticket categorization, dynamic multi-variable priority scoring, telemetry-driven root-cause discovery, and closed-loop DevOps orchestration (Jira, GitHub, Jenkins, Docker).

### 1.2 Problem Decomposition & Sub-Challenges
* **Heuristic Triage Bottleneck**: Human operators frequently misclassify incident severity, allowing catastrophic service failures to languish in general queues while low-impact requests are escalated prematurely.
* **Routing Fragmentation**: SREs lack automated mapping from unstructured ticket text to domain-specific engineering teams (Database Operations, Security Ops, SRE Infrastructure, Network Core).
* **Telemetry Isolation**: Traditional ticketing databases operate isolated from live infrastructure telemetry, preventing immediate correlation between hardware resource saturation ($>90\%$ CPU spikes) and application latency.
* **Governance Gaps**: Service provisioning (IAM roles, SaaS licenses, hardware) and RFC change proposals are frequently executed through fragmented email threads lacking cryptographic auditability.
* **DevOps Disconnect**: Engineers lose valuable time manually authoring incident response tickets in Jira and triggering CI/CD pipelines rather than having immediate two-way bidirectional issue and build synchronization.

### 1.3 Expected Engineering Deliverables
* **Cognitive AI Classifier**: An automated diagnostic engine classifying incidents into 10 operational domains with a dynamic Priority Matrix ($\text{Priority} = \text{Impact} \times \text{Urgency}$) and confidence ratings.
* **ITIL v4 Operations Suite**: Full ITIL v4 lifecycle workflows for Incidents (New $\to$ Assigned $\to$ In Progress $\to$ Pending $\to$ Resolved $\to$ Closed), Service Requests, Problems (RCA), Changes (RFCs), and CMDB Assets.
* **Telemetry & Fault Simulator**: Real-time telemetry gauges displaying CPU, RAM, Disk, and Latency with an automated metric spike injection testing tool.
* **DevOps Orchestration Hub**: Bidirectional Jira ticket synchronization, GitHub commit stream monitoring, and an 11-stage automated Jenkins CI/CD pipeline.
* **Containerized Topology**: Zero-downtime, reproducible 3-tier production containerization orchestrated via Docker Compose and validated across 11 automated Pytest unit tests.

---

## 2. Scope, Engineering Objectives, and Measurable Deliverables

### 2.1 Primary Engineering Objectives
1. **Normalized Relational Architecture**: Design and implement an ACID-compliant relational data model encompassing 16 normalized tables using SQLAlchemy 2.0 and PostgreSQL 16.
2. **Type-Safe Backend Services**: Develop a high-performance RESTful API in Python 3.13 and FastAPI featuring Pydantic v2 validation, JWT authentication, and sub-100ms response latencies.
3. **Interactive Frontend Console**: Construct a responsive, enterprise-grade Single Page Application in React 18 and TypeScript with Tailwind CSS and custom glassmorphic styling.
4. **End-to-End DevOps Scenario**: Synthesize an end-to-end 23-step critical outage demonstration scenario (`INC-1025`) linking infrastructure telemetry breach to automated Jira sync and Jenkins container rollout.
5. **Multi-Container Orchestration**: Package all components into multi-stage production Docker containers orchestrated through `docker-compose.yml`.

### 2.2 Measurable Performance Targets
The platform targets a 65% reduction in incident triage latency, automated P1 response SLA enforcement within 15 minutes, sub-30 minute resolution MTTR for standardized database locking scenarios, and 100% test passing across all core backend routing contracts.

---

## 3. Multi-Tier Requirements Specification, Constraints, and System Assumptions

### 3.1 Functional Requirements Matrix

| Functional Module | Architectural Requirement & Specification |
| :--- | :--- |
| **Incident Desk & Triage** | Provides ticket creation, automated category assignment, priority evaluation, team routing, SLA countdown clocks, internal work notes, and Jira synchronization. |
| **Infrastructure Telemetry** | Streams live host telemetry (CPU %, Memory %, Disk %, Latency ms) and provides interactive threshold breach injection ($>90\%$) triggering automated alerts and P1 incidents. |
| **Service Request Catalog** | Delivers an enterprise catalog for cloud IAM roles, hardware requisitions, and software licenses with status-driven managerial approval gating. |
| **Change Control (CAB)** | Facilitates Request for Change (RFC) submission with automated risk calculation, implementation blueprints, rollback plans, and CAB approval controls. |
| **Problem Management (RCA)** | Correlates recurring incident clusters (e.g. `INC-1001`, `INC-1025`) into root-cause investigation records with published workarounds and permanent fixes. |
| **DevOps & AI Operations Hub** | Orchestrates bidirectional Jira issue synchronization, GitHub commit telemetry, Jenkins 11-stage CI/CD status, and diagnostic runbook recommendation feeds. |

### 3.2 Non-Functional & Quality Attributes
* **Latency & Throughput**: API endpoint execution under 80ms for CRUD operations; real-time dashboard state synchronization.
* **Environmental Parity**: Container-level isolation across Windows, Linux, and Cloud instances without environment configuration drift.
* **Data Integrity & Fault Tolerance**: ACID relational compliance backed by PostgreSQL volume persistence surviving container restarts.
* **Codebase Maintainability**: Decoupled MVC architecture separating database entities, Pydantic schemas, business services, and presentation components.

---

## 4. Rigorous Integration of Core Software Engineering Principles (CSA1011)

* **4.1 Software Development Life Cycle (SDLC)**: Followed an iterative, agile feature-driven development paradigm across 6 distinct phases: requirements analysis $\to$ schema design $\to$ backend REST API $\to$ React SPA $\to$ DevOps pipeline integration $\to$ containerized verification.
* **4.2 Architecture & Design Patterns**: Strict enforcement of 3-tier architectural layering (Presentation, Business Logic, Data Persistence) adhering to the Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).
* **4.3 Relational Schema Engineering**: Comprehensive 3NF normalization across 16 relational entities with cascading foreign keys, unique constraint indexes, and immutable audit trails using SQLAlchemy 2.0.
* **4.4 Software Configuration Management**: Adoption of the Git Flow branching model (`main`, `development`, `feature` branches) with structured Conventional Commits and remote upstream synchronization.
* **4.5 Deployment & Continuous Integration**: Implementation of container-first DevOps engineering: multi-stage Docker builds, docker-compose orchestration, and automated 11-stage Jenkins CI/CD pipeline execution.
* **4.6 Heuristic Algorithm Formulation**: Design of a multi-variable priority evaluation algorithm combining symptom keyword heuristics with impact-urgency matrices.

---

## 5. System Architecture, Layered Decomposition, and Directory Schemas

### 5.1 High-Level Architecture Decomposition

| Architectural Tier | Implementation Technology | Functional Scope |
| :--- | :--- | :--- |
| **Presentation Tier** | React 18 + TypeScript + Vite + Tailwind CSS | Renders the dark glassmorphic operations console, incident queues, telemetry gauges, RFC approvals, and 23-step scenario modal. |
| **Application Tier** | Python 3.13 + FastAPI + Pydantic v2 | Executes business logic, AI diagnostic heuristics, SLA countdown calculation, Jira synchronization, and Jenkins webhooks. |
| **Persistence Tier** | PostgreSQL 16 Alpine + SQLAlchemy 2.0 | Maintains relational integrity across 16 normalized tables with automated seed migration on startup. |
| **DevOps & CI/CD Tier** | Docker Compose + Jenkins 2.568.2 (11 Stages) | Manages multi-container lifecycle, automated testing, image packaging, and deployment health validation. |

### 5.2 Repository Organization
```
ai-powered-it-services/
├── backend/
│   ├── app/
│   │   ├── api/             # REST API routers (incidents, ai, jira, devops, etc.)
│   │   ├── core/            # Config, database engine, security JWT, seed data
│   │   ├── models/          # SQLAlchemy relational entities (16 models)
│   │   ├── schemas/         # Pydantic v2 request/response schemas
│   │   ├── services/        # AI engine, Jira sync, DevOps hub, SLA services
│   │   └── main.py          # FastAPI application entrypoint & lifespan
│   ├── requirements.txt     # Python dependency specifications
│   └── Dockerfile           # Python 3.13-slim container build
├── frontend/
│   ├── src/
│   │   ├── components/      # Sidebar, Topbar, Modals, AI drawer, Scenario runner
│   │   ├── pages/           # Dashboard, Incidents, Assets, Changes, DevOps, etc.
│   │   ├── services/api.ts  # Centralized TypeScript API client wrapper
│   │   ├── App.tsx          # Master routing and layout orchestration
│   │   └── index.css        # Tailwind CSS and glassmorphic styling system
│   ├── Dockerfile           # Multi-stage Node 22 & Nginx Alpine production build
│   └── nginx.conf           # Reverse proxy configuration
├── tests/backend/           # Pytest automated test suite (11 unit tests)
├── docker-compose.yml       # 3-tier container orchestration (frontend, backend, postgres)
├── Jenkinsfile              # 11-stage enterprise CI/CD pipeline
└── README.md                # Comprehensive documentation
```

---

## 6. Cognitive Heuristic Algorithms, Priority Formulations, and Decision Flowcharts

### 6.1 Incident Categorization & Priority Matrix Algorithm
```python
ALGORITHM DiagnoseAndPrioritizeIncident(Ticket T):
    Input: T.title, T.description, T.impact, T.urgency
    Output: Category, Priority, SLA_Deadlines, Assigned_Team, Root_Cause, Action_Plan, Confidence

    1. Category Classification:
       Domain_Keywords = {
           'Database': ['postgres', 'sql', 'deadlock', 'query', 'table', 'lock', 'pool'],
           'Authentication': ['sso', 'saml', 'ldap', 'token', 'login', 'oauth', 'mfa'],
           'Network': ['vpn', 'dns', 'packet', 'latency', 'gateway', 'firewall', 'bgp'],
           'Security': ['ddos', 'breach', 'tls', 'certificate', 'vulnerability', 'cve'],
           'Infrastructure': ['cpu', 'memory', 'disk', 'kernel', 'oom', 'hypervisor']
       }
       Category = MatchHighestFrequencyCategory(T.title + " " + T.description, Domain_Keywords)

    2. Priority Matrix Scoring (Impact x Urgency):
       IF (T.impact == 'High' AND T.urgency == 'High') OR MatchesOutageKeywords(T.description):
           Priority = 'P1' # SLA: 15m Ack, 2h Resolution
       ELSE IF (T.impact == 'High' AND T.urgency == 'Medium') OR (T.impact == 'Medium' AND T.urgency == 'High'):
           Priority = 'P2' # SLA: 30m Ack, 4h Resolution
       ELSE IF (T.impact == 'Medium' AND T.urgency == 'Medium'):
           Priority = 'P3' # SLA: 2h Ack, 8h Resolution
       ELSE:
           Priority = 'P4' # SLA: 8h Ack, 24h Resolution

    3. Support Team Routing & Root-Cause Inference:
       Assigned_Team = MapCategoryToTeam(Category)
       Root_Cause, Action_Plan, Confidence = InferDiagnosticPlaybook(Category, T.description)

    4. Automated Integration Triggers:
       IF Priority == 'P1':
           DispatchJiraIssue(T.incident_number, T.title, 'P1', Assigned_Team)
           BroadcastSREAlert(T.incident_number, T.title)

    RETURN { Category, Priority, Assigned_Team, Root_Cause, Action_Plan, Confidence }
```

---

## 7. Technical Implementation Stack, Version Control, and Deployment Topology

### 7.1 Technical Stack Inventory
* **Frontend Client**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons
* **Backend Service**: Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.0, Uvicorn, Passlib (Bcrypt)
* **Persistence Engine**: PostgreSQL 16 Alpine (Production) / SQLite3 (Local fallback)
* **Containerization**: Docker 26/29, Docker Compose, Nginx Alpine Multi-Stage
* **CI/CD Pipeline**: Jenkins 2.568.2 LTS (11-Stage Declarative Pipeline)
* **Source Control**: Git 2.47, GitHub ([https://github.com/brahmaiah528/ai-powered-it-services](https://github.com/brahmaiah528/ai-powered-it-services))

### 7.2 Version Control History (Git Flow)
1. **Initial Core Architecture**: `830a3b9` &mdash; `feat: complete AI-Powered IT Service Management & DevOps Platform` (80 files, 13,657 insertions)
2. **Container Build Optimization**: `c429794` &mdash; `chore: add frontend .dockerignore`
3. **CI/CD Pipeline Hardening**: `e624304` &mdash; `ci: enhance Jenkinsfile stages for Docker CI runner compatibility`

### 7.3 Production Docker Compose Topology
* **`itsm-frontend`**: Port `80` / `3000` &mdash; Nginx production web server hosting React 18 SPA.
* **`itsm-backend`**: Port `8000` &mdash; FastAPI Python 3.13 service providing REST APIs and Swagger UI.
* **`itsm-postgres`**: Port `5432` &mdash; PostgreSQL 16 database with mounted data volume persistence.

---

## 8. Verification Test Matrix, Executed Assertions, and Empirical Results

| Test ID | Target Test Specification | Expected Assertion | Status / Output |
| :---: | :--- | :--- | :---: |
| **TC-01** | `POST /api/auth/login` with valid user credentials | HTTP 200 + Signed JWT Access Token | **PASS (200 OK)** |
| **TC-02** | `GET /api/incidents` (Retrieve seed queue) | HTTP 200 + Array of 30 seeded incidents | **PASS (200 OK)** |
| **TC-03** | `POST /api/incidents` (AI Auto-Prioritization) | HTTP 201 + Category and P1 matrix calculated | **PASS (201 Created)** |
| **TC-04** | `PATCH /api/incidents/{id}` status to Resolved | HTTP 200 + Resolution notes appended to history | **PASS (200 OK)** |
| **TC-05** | `POST /api/ai/diagnose` (Query analysis) | Category mapped + Confidence $> 80\%$ + Runbook | **PASS (96.5% confidence)** |
| **TC-06** | `POST /api/jira/create-issue` for critical ticket | Jira issue `ITSM-245` created and synced | **PASS (ITSM-245 linked)** |
| **TC-07** | `POST /api/infrastructure/simulate-spike` (94% CPU) | Alert `ALT-94201` generated + Auto P1 logged | **PASS (Alert dispatched)** |
| **TC-08** | Jenkins 11-Stage Pipeline execution | All 11 stages finish with SUCCESS status | **PASS (Build #3 SUCCESS)** |
| **TC-09** | `docker compose up --build -d` | All 3 containers healthy on ports 80, 8000, 5432 | **PASS (All containers Healthy)** |

---

## 9. User Interface Walkthrough and Operational Viewports

* **9.1 Executive Command Dashboard**: Displays live MTTR (38.5m), SLA compliance rate (94.2%), active P1 outage cards, department volume distribution charts, and real-time audit event streams.
* **9.2 Incident Desk & Detail Inspector**: Comprehensive table featuring severity badges (P1–P4), SLA countdown clocks, search filters, and an in-depth incident detail drawer.
* **9.3 Infrastructure Health Telemetry**: Cluster visualization tracking CPU, Memory, Disk, and Latency with an interactive fault injection tool generating live critical incidents.
* **9.4 Service Request Portal**: Self-service catalog for Cloud IAM roles, compute resources, and software entitlements with manager approval routing.
* **9.5 Change Advisory Board (CAB) Control**: RFC submission modal with risk scoring, implementation blueprints, rollback plans, and CAB approval buttons.
* **9.6 Diagnostic Knowledge Base**: Repository of 20 diagnostic runbooks detailing symptoms, root causes, and step-by-step resolution scripts.
* **9.7 DevOps & Jira Integration Hub**: Bidirectional Jira issue status sync, GitHub commit feed, Jenkins 11-stage pipeline stage view, and Docker container health monitors.

---

## 10. Empirical Validation, Build Verification, and Requirement Traceability

* **10.1 Backend Test Automation (Pytest)**: All 11 unit tests in `tests/backend/` passed with 100% success rate in 5.11 seconds, verifying authentication tokens, incident state machines, AI heuristics, and Jira sync endpoints.
* **10.2 Frontend Compilation & Packaging**: The React 18 TypeScript application compiled cleanly with zero linting or type errors, bundling into optimized static assets via Vite in 32.19s.
* **10.3 Jenkins CI/CD Pipeline Execution**: Jenkins Pipeline Build #3 executed all 11 stages (Checkout $\to$ Backend Dependencies $\to$ Frontend Dependencies $\to$ Backend Tests $\to$ Frontend Tests $\to$ Build Frontend $\to$ Build Backend $\to$ Docker Build $\to$ Compose Validation $\to$ Deployment $\to$ Health Check) finishing with status **SUCCESS**.
* **10.4 Requirement Traceability Matrix**:
  * Autonomous Triage: **Verified** (Real-time 10-domain classifier and $\text{Priority} = \text{Impact} \times \text{Urgency}$ matrix).
  * ITIL v4 Operations Suite: **Verified** (Full lifecycle coverage for Incidents, Service Requests, Problems, Changes, and CMDB Assets).
  * Docker Containerization: **Verified** (Multi-container PostgreSQL, FastAPI backend, and React frontend deployment).
  * DevOps Ecosystem: **Verified** (Two-way synchronization with Jira Cloud, GitHub commits, and Jenkins CI/CD).

---

## 11. Engineering Trade-offs, Architectural Comparison, and Design Justification

* **11.1 Dual Database Engine Architecture**: The platform implements dual database engines: SQLite for zero-dependency local developer execution and PostgreSQL 16 for production-grade multi-container deployment with connection pooling. This delivers immediate developer onboarding while maintaining enterprise scalability.
* **11.2 Closed-Loop DevOps Orchestration Justification**: Integrating Jira Cloud and Jenkins directly into the ITSM console eliminates manual context switching for SREs during critical outages, enabling one-click hotfix deployment and automatic ticket resolution.

---

## 12. Societal Imperatives, Sustainable Compute, and UN SDG 9 Alignment

* **12.1 Environmental Sustainability**: Accelerated incident resolution eliminates prolonged CPU saturation on unindexed database clusters, directly minimizing energy consumption and data center carbon footprint.
* **12.2 Societal & Industrial Resilience**: Minimizing downtime in mission-critical enterprise systems safeguards healthcare, financial transactions, and public digital infrastructure against prolonged outages.
* **12.3 SDG 9 Alignment**: Directly advances **UN Sustainable Development Goal 9 (Industry, Innovation & Infrastructure)** through intelligent automation and resilient digital systems.
* **12.4 Professional Accountability**: Immutable audit logging of all operator actions ensures transparency, regulatory compliance, and ethical oversight.

---

## 13. Concluding Remarks, Architectural Constraints, and Future Roadmap

### 13.1 Conclusion
The AI-Powered IT Service Management & Incident Resolution Platform successfully delivers a complete, production-grade IT operations suite. All functional objectives, AI diagnostic capabilities, DevOps integrations, and containerized deployment goals have been verified.

### 13.2 Limitations & Future Roadmap
* **Deep Learning Model Integration**: Incorporate transformer-based LLM embeddings for conversational log analysis and predictive outage forecasting.
* **Multi-Cluster Kubernetes Helm**: Integrate Prometheus / Grafana agents for automated multi-cluster Kubernetes auto-scaling.
* **Enterprise SSO**: OAuth2 / SAML single sign-on integration with enterprise identity providers (Okta, Azure AD).

---

## 14. Individual Contributions and Team Responsibility Breakdown

* **Pramith Maredukonda (192372174)**: Team Lead — FastAPI REST architecture, PostgreSQL relational schemas, Cognitive AI Diagnostic Engine, Jira 2-way sync service, and system documentation.
* **Thonduru Sushma (192325135)**: Frontend Architecture — Executive Command Dashboard, Incident Queue & Detail views, Service Request Catalog, and Change Advisory Board (CAB) review workflows.
* **Chimaladinne Naga Anjali (192372201)**: DevOps & Infrastructure — Multi-stage Docker containerization, 11-stage Jenkins CI/CD pipeline, Git Flow configuration, and Pytest automated testing suite.
* **SRIRAM SASIDHAR SAI (192311276)**: Telemetry & AI Operations — Real-time infrastructure health monitor, live metric spike fault simulation, and conversational AI Runbook Diagnostic Assistant.

---

## 15. Academic and Industry Scholarly References

1. FastAPI Framework, "FastAPI Documentation," tiangolo, 2024. [Online]. Available: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
2. React, "React – The library for web and native user interfaces," Meta Open Source. [Online]. Available: [https://react.dev](https://react.dev)
3. PostgreSQL Global Development Group, "PostgreSQL 16 Documentation," 2024. [Online]. Available: [https://www.postgresql.org/docs](https://www.postgresql.org/docs)
4. Jenkins Project, "Jenkins User Documentation & Pipelines," 2026. [Online]. Available: [https://www.jenkins.io/doc](https://www.jenkins.io/doc)
5. Docker, Inc., "Docker Compose Specification & Multi-stage Builds," 2026. [Online]. Available: [https://docs.docker.com](https://docs.docker.com)
6. ITIL v4 Foundation, "ITIL Foundation: ITIL 4 Edition," AXELOS, 2019.
7. "AI Enhanced Ticket Management System for Optimized Support," ACM Conference on AI-ML Systems, 2025.

---

## 16. Individual Engineering Reflections and Retrospective

* **Architectural Decisions & Module Ownership**: Architecting the unified system using FastAPI, PostgreSQL, and React TypeScript was a decisive factor in achieving both type safety and high runtime efficiency. By decoupling core functionalities into dedicated services (AI diagnostic engine, Jira synchronizer, DevOps tracker, SLA calculator), our team of four was able to independently develop and test modules without merge conflicts or interface incompatibilities.
* **Technical Challenges & Resolutions**: The most intricate engineering challenge was synchronizing the 23-step Critical Database Failure scenario across disparate tools: infrastructure telemetry spike injection, automated alert generation, P1 incident creation, AI heuristic diagnostic scoring, Jira ticket linking, GitHub commit tracking, and Jenkins 11-stage CI/CD pipeline execution. We solved this by developing an automated simulation controller that coordinates the entire recovery lifecycle with real-time feedback.
* **Course Outcome Attainment (CO-6)**: This project provided direct hands-on experience applying core Software Engineering principles (CO-6, Level L6) to enterprise-scale systems — from requirements analysis and relational 3NF schema modeling to containerized deployment, CI/CD automation, and rigorous Pytest validation.

---

## Appendix: Assessment Rubric and Course Outcome Attainment Matrix

| Assessment Criterion | Weightage | Mapped Project Section | Attainment Evidence |
| :--- | :---: | :---: | :--- |
| **Problem Formulation & Scope** | 10 Marks | Section 1 | Clear decomposition of enterprise ITSM latency and DevOps bottlenecks. |
| **Course Knowledge Application** | 20 Marks | Section 4 | Direct application of SDLC, 3-tier MVC, 3NF schema normalization, and Git Flow. |
| **System Design & Methodology** | 20 Marks | Sections 5, 7 | Decoupled 3-tier architecture with FastAPI, PostgreSQL 16, React 18, and Docker. |
| **Modern Toolchain Utilization** | 10 Marks | Sections 7.1, 7.3 | Multi-stage Docker builds, Jenkins 11-stage CI/CD, and Jira Cloud integration. |
| **Verification & Testing Rigor** | 15 Marks | Sections 8, 10 | 11/11 automated Pytest unit tests passing (100%) and Jenkins Build #3 success. |
| **Design Trade-offs & Justification** | 15 Marks | Section 11 | Dual-database engine comparison and closed-loop DevOps orchestration justification. |
| **Broader Impact & Professional Ethics**| 5 Marks | Section 12 | Compute carbon reduction, enterprise resilience, and UN SDG 9 alignment. |
| **Documentation & Retrospective** | 5 Marks | Sections 15, 16 | Formal references, team member breakdown, and reflective retrospectives. |
| **TOTAL** | **100 Marks** | **All Sections** | **Comprehensive Full-Stack Coursework Implementation** |
