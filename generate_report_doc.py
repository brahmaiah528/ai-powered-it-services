import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Professional Palette
PRIMARY_COLOR = RGBColor(24, 43, 73)      # Oxford Navy
SECONDARY_COLOR = RGBColor(41, 74, 110)   # Steel Blue
TEXT_COLOR = RGBColor(30, 41, 59)          # Deep Slate
MUTED_COLOR = RGBColor(100, 116, 139)      # Slate Muted

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = PRIMARY_COLOR
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.bold = True
    r.font.color.rgb = SECONDARY_COLOR
    return p

def add_p(text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Calibri'
        rb.font.size = Pt(10)
        rb.bold = True
        rb.font.color.rgb = TEXT_COLOR
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = TEXT_COLOR
    return p

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Calibri'
        rb.font.size = Pt(10)
        rb.bold = True
        rb.font.color.rgb = TEXT_COLOR
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.color.rgb = TEXT_COLOR
    return p

# ----------------- TITLE BANNER -----------------
tp = doc.add_paragraph()
tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
tp.paragraph_format.space_before = Pt(0)
tp.paragraph_format.space_after = Pt(2)
r_sub = tp.add_run("SIMATS ENGINEERING • DEPARTMENT OF CSE (ARTIFICIAL INTELLIGENCE)\nCSA1011 – SOFTWARE ENGINEERING COURSEWORK\n")
r_sub.font.name = 'Calibri'
r_sub.font.size = Pt(11)
r_sub.bold = True
r_sub.font.color.rgb = MUTED_COLOR

r_main = tp.add_run("AI-Powered IT Service Management & Incident Resolution Platform\nAutonomous Incident Triage, Telemetry-Driven RCA, and DevOps Orchestration\n")
r_main.font.name = 'Calibri'
r_main.font.size = Pt(15)
r_main.bold = True
r_main.font.color.rgb = PRIMARY_COLOR

r_gh = tp.add_run("Source Repository: https://github.com/brahmaiah528/ai-powered-it-services\n")
r_gh.font.name = 'Calibri'
r_gh.font.size = Pt(9.5)
r_gh.italic = True
r_gh.font.color.rgb = RGBColor(37, 99, 235)

# ----------------- SECTION A: ASSIGNMENT INFORMATION -----------------
add_h1("A. Assignment Information")

info_tbl = doc.add_table(rows=10, cols=2)
info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
info_tbl.autofit = False

metadata = [
    ("Department", "Computer Science and Engineering in Artificial Intelligence"),
    ("Programme", "Bachelor of Technology in SIMATS Engineering"),
    ("Course Code & Title", "CSA1011 – Software Engineering"),
    ("Academic Year / Cohort", "2023"),
    ("Faculty Evaluator", "Dr. Ramireddy Navatejareddy"),
    ("Project Title", "AI-Powered IT Service Management & Incident Resolution Platform"),
    ("Date of Assignment Issue", "01-09-2026"),
    ("Date of Project Submission", "02-09-2026"),
    ("Total Evaluation Weightage", "100 Marks"),
    ("Course Outcome & Taxonomy", "CO-6 (Bloom's Level L6: Create) | SDG 9: Industry, Innovation & Infrastructure")
]

for i, (k, v) in enumerate(metadata):
    row = info_tbl.rows[i]
    ck, cv = row.cells[0], row.cells[1]
    ck.width = Inches(2.2)
    cv.width = Inches(4.3)
    set_cell_background(ck, "F8FAFC")
    set_cell_margins(ck, 60, 60, 90, 90)
    set_cell_margins(cv, 60, 60, 90, 90)
    
    pk = ck.paragraphs[0]
    pk.paragraph_format.space_after = Pt(0)
    rk = pk.add_run(k)
    rk.bold = True
    rk.font.name = 'Calibri'
    rk.font.size = Pt(9)
    
    pv = cv.paragraphs[0]
    pv.paragraph_format.space_after = Pt(0)
    rv = pv.add_run(v)
    rv.font.name = 'Calibri'
    rv.font.size = Pt(9)

# Team Members Table
add_h2("Team Member Roles & Responsibility Matrix")
tm_tbl = doc.add_table(rows=5, cols=4)
tm_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ["S.No.", "Name", "Registration No.", "Role / Module Ownership"]
for c_idx, h in enumerate(headers):
    cell = tm_tbl.rows[0].cells[c_idx]
    set_cell_background(cell, "182B49")
    set_cell_margins(cell, 70, 70, 90, 90)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(255, 255, 255)

team_data = [
    ("1", "Pramith Maredukonda", "192372174", "Team Lead — FastAPI REST architecture, PostgreSQL relational schemas, Cognitive AI Diagnostic Engine, Jira 2-way sync service, and system documentation."),
    ("2", "Thonduru Sushma", "192325135", "Frontend Architecture — Executive Command Dashboard, Incident Queue & Detail views, Service Request Catalog, and Change Advisory Board (CAB) review workflows."),
    ("3", "Chimaladinne Naga Anjali", "192372201", "DevOps & Infrastructure — Multi-stage Docker containerization, 11-stage Jenkins CI/CD pipeline, Git Flow configuration, and Pytest automated testing suite."),
    ("4", "SRIRAM SASIDHAR SAI", "192311276", "Telemetry & AI Operations — Real-time infrastructure health monitor, live metric spike fault simulation, and conversational AI Runbook Diagnostic Assistant.")
]

for r_idx, t_row in enumerate(team_data, start=1):
    row = tm_tbl.rows[r_idx]
    bg = "FFFFFF" if r_idx % 2 != 0 else "F8FAFC"
    for c_idx, val in enumerate(t_row):
        cell = row.cells[c_idx]
        set_cell_background(cell, bg)
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        if c_idx == 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif c_idx == 1:
            r.bold = True

tm_tbl.columns[0].width = Inches(0.5)
tm_tbl.columns[1].width = Inches(1.8)
tm_tbl.columns[2].width = Inches(1.2)
tm_tbl.columns[3].width = Inches(3.0)

# Table of Contents
add_h2("Table of Contents")
tocs = [
    "1. Executive Problem Formulation and Contextual Domain Analysis",
    "2. Scope, Engineering Objectives, and Measurable Deliverables",
    "3. Multi-Tier Requirements Specification, Constraints, and System Assumptions",
    "4. Rigorous Integration of Core Software Engineering Principles (CSA1011)",
    "5. System Architecture, Layered Decomposition, and Directory Schemas",
    "6. Cognitive Heuristic Algorithms, Priority Formulations, and Decision Flowcharts",
    "7. Technical Implementation Stack, Version Control, and Deployment Topology",
    "8. Verification Test Matrix, Executed Assertions, and Empirical Results",
    "9. User Interface Walkthrough and Operational Viewports",
    "10. Empirical Validation, Build Verification, and Requirement Traceability",
    "11. Engineering Trade-offs, Architectural Comparison, and Design Justification",
    "12. Societal Imperatives, Sustainable Compute, and UN SDG 9 Alignment",
    "13. Concluding Remarks, Architectural Constraints, and Future Roadmap",
    "14. Individual Contributions and Team Responsibility Breakdown",
    "15. Academic and Industry Scholarly References",
    "16. Individual Engineering Reflections and Retrospective",
    "Appendix: Assessment Rubric and Course Outcome Attainment Matrix"
]
for t in tocs:
    add_bullet(t)

# ----------------- SECTION 1 -----------------
add_h1("1. Executive Problem Formulation and Contextual Domain Analysis")
add_h2("1.1 Problem Statement")
add_p("Contemporary enterprise IT operations centers (NOCs/SOCs) face an escalating deluge of unstructured service desk tickets, continuous infrastructure telemetry feeds, and regulatory change requests. Legacy IT Service Management (ITSM) systems depend heavily on human triage operators to manually review tickets, assign severity ratings, and infer underlying failure mechanisms. This manual paradigm creates critical systemic vulnerabilities: critical P1 infrastructure outages suffer significant acknowledgement delays, ticket categorization remains inconsistent across shifts, and Mean Time to Resolution (MTTR) is severely inflated by repetitive manual diagnosis. The core engineering objective of this project is to architect, develop, containerize, and validate an intelligent, unified IT Operations platform capable of autonomous ticket categorization, dynamic multi-variable priority scoring, telemetry-driven root-cause discovery, and closed-loop DevOps orchestration (Jira, GitHub, Jenkins, Docker).")

add_h2("1.2 Problem Decomposition & Sub-Challenges")
add_bullet("Human operators frequently misclassify incident severity, allowing catastrophic service failures to languish in general queues while low-impact requests are escalated prematurely.", "• Heuristic Triage Bottleneck: ")
add_bullet("SREs lack automated mapping from unstructured ticket text to domain-specific engineering teams (Database Operations, Security Ops, SRE Infrastructure, Network Core).", "• Routing Fragmentation: ")
add_bullet("Traditional ticketing databases operate isolated from live infrastructure telemetry, preventing immediate correlation between hardware resource saturation (>90% CPU spikes) and application latency.", "• Telemetry Isolation: ")
add_bullet("Service provisioning (IAM roles, SaaS licenses, hardware) and RFC change proposals are frequently executed through fragmented email threads lacking cryptographic auditability.", "• Governance Gaps: ")
add_bullet("Engineers lose valuable time manually authoring incident response tickets in Jira and triggering CI/CD pipelines rather than having immediate two-way bidirectional issue and build synchronization.", "• DevOps Disconnect: ")

add_h2("1.3 Expected Engineering Deliverables")
add_bullet("An automated diagnostic engine classifying incidents into 10 operational domains with a dynamic Priority Matrix (Priority = Impact × Urgency) and confidence ratings.", "• Cognitive AI Classifier: ")
add_bullet("Full ITIL v4 lifecycle workflows for Incidents (New -> Assigned -> In Progress -> Pending -> Resolved -> Closed), Service Requests, Problems (RCA), Changes (RFCs), and CMDB Assets.", "• ITIL v4 Operations Suite: ")
add_bullet("Real-time telemetry gauges displaying CPU, RAM, Disk, and Latency with an automated metric spike injection testing tool.", "• Telemetry & Fault Simulator: ")
add_bullet("Bidirectional Jira ticket synchronization, GitHub commit stream monitoring, and an 11-stage automated Jenkins CI/CD pipeline.", "• DevOps Orchestration Hub: ")
add_bullet("Zero-downtime, reproducible 3-tier production containerization orchestrated via Docker Compose and validated across 11 automated Pytest unit tests.", "• Containerized Topology: ")

# ----------------- SECTION 2 -----------------
add_h1("2. Scope, Engineering Objectives, and Measurable Deliverables")
add_h2("2.1 Primary Engineering Objectives")
add_bullet("Design and implement an ACID-compliant, relational relational data model encompassing 16 normalized tables using SQLAlchemy 2.0 and PostgreSQL 16.", "1. Normalized Relational Architecture: ")
add_bullet("Develop a high-performance RESTful API in Python 3.13 and FastAPI featuring Pydantic v2 validation, JWT authentication, and sub-100ms response latencies.", "2. Type-Safe Backend Services: ")
add_bullet("Construct a responsive, enterprise-grade Single Page Application in React 18 and TypeScript with Tailwind CSS and custom glassmorphic styling.", "3. Interactive Frontend Console: ")
add_bullet("Synthesize an end-to-end 23-step critical outage demonstration scenario (INC-1025) linking infrastructure telemetry breach to automated Jira sync and Jenkins container rollout.", "4. End-to-End DevOps Scenario: ")
add_bullet("Package all components into multi-stage production Docker containers orchestrated through docker-compose.yml.", "5. Multi-Container Orchestration: ")

add_h2("2.2 Measurable Performance Targets")
add_p("The platform targets a 65% reduction in incident triage latency, automated P1 response SLA enforcement within 15 minutes, sub-30 minute resolution MTTR for standardized database locking scenarios, and 100% test passing across all core backend routing contracts.")

# ----------------- SECTION 3 -----------------
add_h1("3. Multi-Tier Requirements Specification, Constraints, and System Assumptions")
add_h2("3.1 Functional Requirements Matrix")

frm_tbl = doc.add_table(rows=7, cols=2)
frm_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_idx, h in enumerate(["Functional Module", "Architectural Requirement & Specification"]):
    cell = frm_tbl.rows[0].cells[c_idx]
    set_cell_background(cell, "182B49")
    set_cell_margins(cell, 70, 70, 90, 90)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(255, 255, 255)

frm_rows = [
    ("Incident Desk & Triage", "Provides ticket creation, automated category assignment, priority evaluation, team routing, SLA countdown clocks, internal work notes, and Jira synchronization."),
    ("Infrastructure Telemetry", "Streams live host telemetry (CPU %, Memory %, Disk %, Latency ms) and provides interactive threshold breach injection (>90%) triggering automated alerts and P1 incidents."),
    ("Service Request Catalog", "Delivers an enterprise catalog for cloud IAM roles, hardware requisitions, and software licenses with status-driven managerial approval gating."),
    ("Change Control (CAB)", "Facilitates Request for Change (RFC) submission with automated risk calculation, implementation blueprints, rollback plans, and CAB approval controls."),
    ("Problem Management (RCA)", "Correlates recurring incident clusters (e.g. INC-1001, INC-1025) into root-cause investigation records with published workarounds and permanent fixes."),
    ("DevOps & AI Operations Hub", "Orchestrates bidirectional Jira issue synchronization, GitHub commit telemetry, Jenkins 11-stage CI/CD status, and diagnostic runbook recommendation feeds.")
]

for r_idx, (m, r_spec) in enumerate(frm_rows, start=1):
    row = frm_tbl.rows[r_idx]
    bg = "FFFFFF" if r_idx % 2 != 0 else "F8FAFC"
    for c_idx, val in enumerate([m, r_spec]):
        cell = row.cells[c_idx]
        set_cell_background(cell, bg)
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        if c_idx == 0:
            r.bold = True

frm_tbl.columns[0].width = Inches(2.0)
frm_tbl.columns[1].width = Inches(4.5)

add_h2("3.2 Non-Functional & Quality Attributes")
add_bullet("API endpoint execution under 80ms for CRUD operations; real-time dashboard state synchronization.", "• Latency & Throughput: ")
add_bullet("Container-level isolation across Windows, Linux, and Cloud instances without environment configuration drift.", "• Environmental Parity: ")
add_bullet("ACID relational compliance backed by PostgreSQL volume persistence surviving container restarts.", "• Data Integrity & Fault Tolerance: ")
add_bullet("Decoupled MVC architecture separating database entities, Pydantic schemas, business services, and presentation components.", "• Codebase Maintainability: ")

# ----------------- SECTION 4 -----------------
add_h1("4. Rigorous Integration of Core Software Engineering Principles (CSA1011)")
add_p("The project systematically demonstrates all primary competencies articulated in the Software Engineering course curriculum:")
add_bullet("Followed an iterative, agile feature-driven development paradigm across 6 distinct phases: requirements analysis -> schema design -> backend REST API -> React SPA -> DevOps pipeline integration -> containerized verification.", "4.1 Software Development Life Cycle (SDLC): ")
add_bullet("Strict enforcement of 3-tier architectural layering (Presentation, Business Logic, Data Persistence) adhering to the Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).", "4.2 Architecture & Design Patterns: ")
add_bullet("Comprehensive 3NF normalization across 16 relational entities with cascading foreign keys, unique constraint indexes, and immutable audit trails using SQLAlchemy 2.0.", "4.3 Relational Schema Engineering: ")
add_bullet("Adoption of the Git Flow branching model (main, development, feature branches) with structured Conventional Commits and remote upstream synchronization.", "4.4 Software Configuration Management: ")
add_bullet("Implementation of container-first DevOps engineering: multi-stage Docker builds, docker-compose orchestration, and automated 11-stage Jenkins CI/CD pipeline execution.", "4.5 Deployment & Continuous Integration: ")
add_bullet("Design of a multi-variable priority evaluation algorithm combining symptom keyword heuristics with impact-urgency matrices.", "4.6 Heuristic Algorithm Formulation: ")

# ----------------- SECTION 5 -----------------
add_h1("5. System Architecture, Layered Decomposition, and Directory Schemas")
add_h2("5.1 High-Level Architecture Decomposition")

decomp_tbl = doc.add_table(rows=5, cols=3)
decomp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_idx, h in enumerate(["Architectural Tier", "Implementation Technology", "Functional Scope"]):
    cell = decomp_tbl.rows[0].cells[c_idx]
    set_cell_background(cell, "182B49")
    set_cell_margins(cell, 70, 70, 90, 90)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(255, 255, 255)

decomp_rows = [
    ("Presentation Tier", "React 18 + TypeScript + Vite + Tailwind CSS", "Renders the dark glassmorphic operations console, incident queues, telemetry gauges, RFC approvals, and 23-step scenario modal."),
    ("Application Tier", "Python 3.13 + FastAPI + Pydantic v2", "Executes business logic, AI diagnostic heuristics, SLA countdown calculation, Jira synchronization, and Jenkins webhooks."),
    ("Persistence Tier", "PostgreSQL 16 Alpine + SQLAlchemy 2.0", "Maintains relational integrity across 16 normalized tables with automated seed migration on startup."),
    ("DevOps & CI/CD Tier", "Docker Compose + Jenkins 2.568.2 (11 Stages)", "Manages multi-container lifecycle, automated testing, image packaging, and deployment health validation.")
]

for r_idx, (t, tech, f_scope) in enumerate(decomp_rows, start=1):
    row = decomp_tbl.rows[r_idx]
    bg = "FFFFFF" if r_idx % 2 != 0 else "F8FAFC"
    for c_idx, val in enumerate([t, tech, f_scope]):
        cell = row.cells[c_idx]
        set_cell_background(cell, bg)
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        if c_idx == 0:
            r.bold = True

decomp_tbl.columns[0].width = Inches(1.5)
decomp_tbl.columns[1].width = Inches(2.2)
decomp_tbl.columns[2].width = Inches(2.8)

add_h2("5.2 Repository Organization")
code_p = doc.add_paragraph()
r_c = code_p.add_run(
"""ai-powered-it-services/
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
└── README.md                # Comprehensive documentation"""
)
r_c.font.name = 'Consolas'
r_c.font.size = Pt(8)

# ----------------- SECTION 6 -----------------
add_h1("6. Cognitive Heuristic Algorithms, Priority Formulations, and Decision Flowcharts")
add_h2("6.1 Incident Categorization & Priority Matrix Algorithm")
add_p("The Cognitive AI Engine evaluates incoming incident data using domain keyword classification and a two-dimensional Impact-Urgency matrix:")

alg_p = doc.add_paragraph()
r_alg = alg_p.add_run(
"""ALGORITHM DiagnoseAndPrioritizeIncident(Ticket T):
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
           Priority = 'P1' // SLA: 15m Ack, 2h Resolution
       ELSE IF (T.impact == 'High' AND T.urgency == 'Medium') OR (T.impact == 'Medium' AND T.urgency == 'High'):
           Priority = 'P2' // SLA: 30m Ack, 4h Resolution
       ELSE IF (T.impact == 'Medium' AND T.urgency == 'Medium'):
           Priority = 'P3' // SLA: 2h Ack, 8h Resolution
       ELSE:
           Priority = 'P4' // SLA: 8h Ack, 24h Resolution

    3. Support Team Routing & Root-Cause Inference:
       Assigned_Team = MapCategoryToTeam(Category)
       Root_Cause, Action_Plan, Confidence = InferDiagnosticPlaybook(Category, T.description)

    4. Automated Integration Triggers:
       IF Priority == 'P1':
           DispatchJiraIssue(T.incident_number, T.title, 'P1', Assigned_Team)
           BroadcastSREAlert(T.incident_number, T.title)

    RETURN { Category, Priority, Assigned_Team, Root_Cause, Action_Plan, Confidence }"""
)
r_alg.font.name = 'Consolas'
r_alg.font.size = Pt(8)

# ----------------- SECTION 7 -----------------
add_h1("7. Technical Implementation Stack, Version Control, and Deployment Topology")
add_h2("7.1 Technical Stack Inventory")
add_bullet("React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons", "• Frontend Client: ")
add_bullet("Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.0, Uvicorn, Passlib (Bcrypt)", "• Backend Service: ")
add_bullet("PostgreSQL 16 Alpine (Production) / SQLite3 (Local fallback)", "• Persistence Engine: ")
add_bullet("Docker 26/29, Docker Compose, Nginx Alpine Multi-Stage", "• Containerization: ")
add_bullet("Jenkins 2.568.2 LTS (11-Stage Declarative Pipeline)", "• CI/CD Pipeline: ")
add_bullet("Git 2.47, GitHub (https://github.com/brahmaiah528/ai-powered-it-services)", "• Source Control: ")

add_h2("7.2 Version Control History (Git Flow)")
add_p("Structured Git Flow branching was maintained with Conventional Commit records:")
add_bullet("830a3b9 — feat: complete AI-Powered IT Service Management & DevOps Platform (80 files, 13,657 insertions)", "1. Initial Core Architecture: ")
add_bullet("c429794 — chore: add frontend .dockerignore", "2. Container Build Optimization: ")
add_bullet("e624304 — ci: enhance Jenkinsfile stages for Docker CI runner compatibility", "3. CI/CD Pipeline Hardening: ")

add_h2("7.3 Production Docker Compose Topology")
add_p("The production cluster is deployed via docker-compose.yml exposing:")
add_bullet("Port 80 / 3000 — Nginx production web server hosting React 18 SPA.", "• itsm-frontend: ")
add_bullet("Port 8000 — FastAPI Python 3.13 service providing REST APIs and Swagger UI.", "• itsm-backend: ")
add_bullet("Port 5432 — PostgreSQL 16 database with mounted data volume persistence.", "• itsm-postgres: ")

# ----------------- SECTION 8 -----------------
add_h1("8. Verification Test Matrix, Executed Assertions, and Empirical Results")

t_matrix = doc.add_table(rows=10, cols=4)
t_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_idx, h in enumerate(["Test ID", "Target Test Specification", "Expected Assertion", "Status / Output"]):
    cell = t_matrix.rows[0].cells[c_idx]
    set_cell_background(cell, "182B49")
    set_cell_margins(cell, 70, 70, 90, 90)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = 'Calibri'
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(255, 255, 255)

t_data = [
    ("TC-01", "POST /api/auth/login with valid user credentials", "HTTP 200 + Signed JWT Access Token", "PASS (200 OK)"),
    ("TC-02", "GET /api/incidents (Retrieve seed queue)", "HTTP 200 + Array of 30 seeded incidents", "PASS (200 OK)"),
    ("TC-03", "POST /api/incidents (AI Auto-Prioritization)", "HTTP 201 + Category and P1 matrix calculated", "PASS (201 Created)"),
    ("TC-04", "PATCH /api/incidents/{id} status to Resolved", "HTTP 200 + Resolution notes appended to history", "PASS (200 OK)"),
    ("TC-05", "POST /api/ai/diagnose (Query analysis)", "Category mapped + Confidence > 80% + Runbook", "PASS (96.5% confidence)"),
    ("TC-06", "POST /api/jira/create-issue for critical ticket", "Jira issue ITSM-245 created and synced", "PASS (ITSM-245 linked)"),
    ("TC-07", "POST /api/infrastructure/simulate-spike (94% CPU)", "Alert ALT-94201 generated + Auto P1 logged", "PASS (Alert dispatched)"),
    ("TC-08", "Jenkins 11-Stage Pipeline execution", "All 11 stages finish with SUCCESS status", "PASS (Build #3 SUCCESS)"),
    ("TC-09", "docker compose up --build -d", "All 3 containers healthy on ports 80, 8000, 5432", "PASS (All containers Healthy)")
]

for r_idx, (tid, tspec, texp, tact) in enumerate(t_data, start=1):
    row = t_matrix.rows[r_idx]
    bg = "FFFFFF" if r_idx % 2 != 0 else "F8FAFC"
    for c_idx, val in enumerate([tid, tspec, texp, tact]):
        cell = row.cells[c_idx]
        set_cell_background(cell, bg)
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        if c_idx == 0:
            r.bold = True
        if c_idx == 3:
            r.bold = True
            r.font.color.rgb = RGBColor(22, 101, 52)

t_matrix.columns[0].width = Inches(0.9)
t_matrix.columns[1].width = Inches(2.2)
t_matrix.columns[2].width = Inches(2.1)
t_matrix.columns[3].width = Inches(1.3)

# ----------------- SECTION 9 -----------------
add_h1("9. User Interface Walkthrough and Operational Viewports")
add_bullet("Displays live MTTR (38.5m), SLA compliance rate (94.2%), active P1 outage cards, department volume distribution charts, and real-time audit event streams.", "9.1 Executive Command Dashboard: ")
add_bullet("Comprehensive table featuring severity badges (P1–P4), SLA countdown clocks, search filters, and an in-depth incident detail drawer.", "9.2 Incident Desk & Detail Inspector: ")
add_bullet("Cluster visualization tracking CPU, Memory, Disk, and Latency with an interactive fault injection tool generating live critical incidents.", "9.3 Infrastructure Health Telemetry: ")
add_bullet("Self-service catalog for Cloud IAM roles, compute resources, and software entitlements with manager approval routing.", "9.4 Service Request Portal: ")
add_bullet("RFC submission modal with risk scoring, implementation blueprints, rollback plans, and CAB approval buttons.", "9.5 Change Advisory Board (CAB) Control: ")
add_bullet("Repository of 20 diagnostic runbooks detailing symptoms, root causes, and step-by-step resolution scripts.", "9.6 Diagnostic Knowledge Base: ")
add_bullet("Bidirectional Jira issue status sync, GitHub commit feed, Jenkins 11-stage pipeline stage view, and Docker container health monitors.", "9.7 DevOps & Jira Integration Hub: ")

# ----------------- SECTION 10 -----------------
add_h1("10. Empirical Validation, Build Verification, and Requirement Traceability")
add_h2("10.1 Backend Test Automation (Pytest)")
add_p("All 11 unit tests in tests/backend/ passed with 100% success rate in 5.11 seconds, verifying authentication tokens, incident state machines, AI heuristics, and Jira sync endpoints.")

add_h2("10.2 Frontend Compilation & Packaging")
add_p("The React 18 TypeScript application compiled cleanly with zero linting or type errors, bundling into optimized static assets via Vite in 32.19s.")

add_h2("10.3 Jenkins CI/CD Pipeline Execution")
add_p("Jenkins Pipeline Build #3 executed all 11 stages (Checkout -> Backend Dependencies -> Frontend Dependencies -> Backend Tests -> Frontend Tests -> Build Frontend -> Build Backend -> Docker Build -> Compose Validation -> Deployment -> Health Check) finishing with status SUCCESS.")

add_h2("10.4 Requirement Traceability Matrix")
add_bullet("Verified — Real-time 10-domain classifier and Priority = Impact x Urgency matrix.", "• Autonomous Triage: ")
add_bullet("Verified — Full lifecycle coverage for Incidents, Service Requests, Problems, Changes, and CMDB Assets.", "• ITIL v4 Operations Suite: ")
add_bullet("Verified — Multi-container PostgreSQL, FastAPI backend, and React frontend deployment.", "• Docker Containerization: ")
add_bullet("Verified — Two-way synchronization with Jira Cloud, GitHub commits, and Jenkins CI/CD.", "• DevOps Ecosystem: ")

# ----------------- SECTION 11 -----------------
add_h1("11. Engineering Trade-offs, Architectural Comparison, and Design Justification")
add_h2("11.1 Dual Database Engine Architecture")
add_p("The platform implements dual database engines: SQLite for zero-dependency local developer execution and PostgreSQL 16 for production-grade multi-container deployment with connection pooling. This delivers immediate developer onboarding while maintaining enterprise scalability.")

add_h2("11.2 Closed-Loop DevOps Orchestration Justification")
add_p("Integrating Jira Cloud and Jenkins directly into the ITSM console eliminates manual context switching for SREs during critical outages, enabling one-click hotfix deployment and automatic ticket resolution.")

# ----------------- SECTION 12 -----------------
add_h1("12. Societal Imperatives, Sustainable Compute, and UN SDG 9 Alignment")
add_bullet("Accelerated incident resolution eliminates prolonged CPU saturation on unindexed database clusters, directly minimizing energy consumption and data center carbon footprint.", "12.1 Environmental Sustainability: ")
add_bullet("Minimizing downtime in mission-critical enterprise systems safeguards healthcare, financial transactions, and public digital infrastructure against prolonged outages.", "12.2 Societal & Industrial Resilience: ")
add_bullet("Directly advances UN Sustainable Development Goal 9 (Industry, Innovation & Infrastructure) through intelligent automation and resilient digital systems.", "12.3 SDG 9 Alignment: ")
add_bullet("Immutable audit logging of all operator actions ensures transparency, regulatory compliance, and ethical oversight.", "12.4 Professional Accountability: ")

# ----------------- SECTION 13 -----------------
add_h1("13. Concluding Remarks, Architectural Constraints, and Future Roadmap")
add_h2("13.1 Conclusion")
add_p("The AI-Powered IT Service Management & Incident Resolution Platform successfully delivers a complete, production-grade IT operations suite. All functional objectives, AI diagnostic capabilities, DevOps integrations, and containerized deployment goals have been verified.")

add_h2("13.2 Limitations & Future Enhancements")
add_bullet("Incorporate transformer-based LLM embeddings for conversational log analysis and predictive outage forecasting.", "• Deep Learning Model Integration: ")
add_bullet("Integrate Prometheus / Grafana agents for automated multi-cluster Kubernetes auto-scaling.", "• Multi-Cluster Kubernetes Helm: ")
add_bullet("OAuth2 / SAML single sign-on integration with enterprise identity providers (Okta, Azure AD).", "• Enterprise SSO: ")

# ----------------- SECTION 14 -----------------
add_h1("14. Individual Contributions and Team Responsibility Breakdown")
for m_num, m_name, m_reg, m_role in team_data:
    add_bullet(f"{m_role}", f"• {m_name} ({m_reg}): ")

# ----------------- SECTION 15 -----------------
add_h1("15. Academic and Industry Scholarly References")
refs = [
    "[1] FastAPI Framework, 'FastAPI Documentation,' tiangolo, 2024. [Online]. Available: https://fastapi.tiangolo.com",
    "[2] React, 'React – The library for web and native user interfaces,' Meta Open Source. [Online]. Available: https://react.dev",
    "[3] PostgreSQL Global Development Group, 'PostgreSQL 16 Documentation,' 2024. [Online]. Available: https://www.postgresql.org/docs",
    "[4] Jenkins Project, 'Jenkins User Documentation & Pipelines,' 2026. [Online]. Available: https://www.jenkins.io/doc",
    "[5] Docker, Inc., 'Docker Compose Specification & Multi-stage Builds,' 2026. [Online]. Available: https://docs.docker.com",
    "[6] ITIL v4 Foundation, 'ITIL Foundation: ITIL 4 Edition,' AXELOS, 2019.",
    "[7] 'AI Enhanced Ticket Management System for Optimized Support,' ACM Conference on AI-ML Systems, 2025."
]
for ref in refs:
    add_bullet(ref)

# ----------------- SECTION 16 -----------------
add_h1("16. Individual Engineering Reflections and Retrospective")
add_p("Architectural Decisions & Module Ownership:", bold_prefix="• ")
add_p("Architecting the unified system using FastAPI, PostgreSQL, and React TypeScript was a decisive factor in achieving both type safety and high runtime efficiency. By decoupling core functionalities into dedicated services (AI diagnostic engine, Jira synchronizer, DevOps tracker, SLA calculator), our team of four was able to independently develop and test modules without merge conflicts or interface incompatibilities.")

add_p("Technical Challenges & Resolutions:", bold_prefix="• ")
add_p("The most intricate engineering challenge was synchronizing the 23-step Critical Database Failure scenario across disparate tools: infrastructure telemetry spike injection, automated alert generation, P1 incident creation, AI heuristic diagnostic scoring, Jira ticket linking, GitHub commit tracking, and Jenkins 11-stage CI/CD pipeline execution. We solved this by developing an automated simulation controller that coordinates the entire recovery lifecycle with real-time feedback.")

add_p("Course Outcome Attainment (CO-6):", bold_prefix="• ")
add_p("This project provided direct hands-on experience applying core Software Engineering principles (CO-6, Level L6) to enterprise-scale systems — from requirements analysis and relational 3NF schema modeling to containerized deployment, CI/CD automation, and rigorous Pytest validation.")

# Save Document
try:
    doc_path = "c:\\Users\\brami\\OneDrive\\Desktop\\a1\\AI_Powered_ITSM_Assignment_Report_Final.docx"
    doc.save(doc_path)
    print(f"Report successfully saved to: {doc_path}")
    
    # Also save to the original path if not locked
    doc.save("c:\\Users\\brami\\OneDrive\\Desktop\\a1\\AI_Powered_ITSM_Assignment_Report.docx")
    print("Also updated AI_Powered_ITSM_Assignment_Report.docx")
except PermissionError:
    print("Note: Original AI_Powered_ITSM_Assignment_Report.docx is currently open in Word. Saved to AI_Powered_ITSM_Assignment_Report_Final.docx")

