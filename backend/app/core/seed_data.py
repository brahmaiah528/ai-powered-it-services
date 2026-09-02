from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.models import (
    Department, BusinessUnit, User, UserRole, Incident, IncidentPriority, IncidentStatus,
    ServiceRequest, ServiceRequestStatus, Problem, ProblemStatus, Change, ChangeType, ChangeStatus,
    Asset, AssetType, AssetStatus, InfrastructureNode, HealthStatus, Alert, AlertSeverity,
    KnowledgeArticle, Notification, AuditLog, SLAPolicy, JiraIssueLink, Comment
)
from app.core.security import get_password_hash
from app.services.sla_service import calculate_sla_deadlines, calculate_priority

def seed_database(db: Session):
    # Check if already seeded
    if db.query(User).first():
        return

    now = datetime.now(timezone.utc)

    # 1. Departments & Business Units
    dept_names = [
        ("DevOps & Site Reliability", "Cloud infrastructure, CI/CD pipelines, container runtime, and high availability"),
        ("Cyber Security & SOC", "Information security, identity access management, threat detection, and firewall compliance"),
        ("Enterprise Database Systems", "PostgreSQL, MySQL, Oracle clusters, replication, and data warehousing"),
        ("Cloud Platform Engineering", "Kubernetes, AWS/GCP architecture, microservices, and serverless compute"),
        ("Corporate IT Service Desk", "End-user support, hardware provisioning, enterprise software licenses, and VPN")
    ]
    departments = []
    for name, desc in dept_names:
        d = Department(name=name, description=desc)
        db.add(d)
        departments.append(d)
    db.flush()

    # 2. SLA Policies
    sla_configs = [
        (IncidentPriority.P1, 15, 120, "Critical Severity SLA: 15min response, 2hr resolution"),
        (IncidentPriority.P2, 30, 240, "High Severity SLA: 30min response, 4hr resolution"),
        (IncidentPriority.P3, 120, 480, "Medium Severity SLA: 2hr response, 8hr resolution"),
        (IncidentPriority.P4, 480, 1440, "Low Severity SLA: 8hr response, 24hr resolution"),
    ]
    for prio, resp, res, desc in sla_configs:
        db.add(SLAPolicy(priority=prio, response_time_minutes=resp, resolution_time_minutes=res, description=desc))

    # 3. 10 Realistic Users
    hashed_pwd = get_password_hash("admin123")
    user_data = [
        ("admin@enterprise.org", "admin", "Marcus Vance (Global Admin)", UserRole.ADMINISTRATOR, departments[0].id, "Principal Systems Architect"),
        ("manager@enterprise.org", "itmanager", "Elena Rostova (IT Operations Manager)", UserRole.IT_MANAGER, departments[4].id, "Head of IT Operations"),
        ("sre-lead@enterprise.org", "srelead", "Sarah Connor (Senior SRE)", UserRole.SERVICE_DESK_AGENT, departments[0].id, "Staff Site Reliability Engineer"),
        ("dba-lead@enterprise.org", "dbalead", "Rajesh Kumar (Principal DBA)", UserRole.SERVICE_DESK_AGENT, departments[2].id, "Lead Database Administrator"),
        ("sec-analyst@enterprise.org", "secanalyst", "Chen Wei (SOC Lead Analyst)", UserRole.SERVICE_DESK_AGENT, departments[1].id, "Senior Security Analyst"),
        ("agent1@enterprise.org", "agent1", "Jordan Taylor (Tier 2 Support)", UserRole.SERVICE_DESK_AGENT, departments[4].id, "Senior Service Desk Specialist"),
        ("agent2@enterprise.org", "agent2", "Maya Lin (Cloud Ops Agent)", UserRole.SERVICE_DESK_AGENT, departments[3].id, "Cloud Operations Specialist"),
        ("user1@enterprise.org", "user1", "Alex Morgan (Product Manager)", UserRole.END_USER, departments[0].id, "Senior Product Manager"),
        ("user2@enterprise.org", "user2", "David Kim (Lead Developer)", UserRole.END_USER, departments[3].id, "Staff Software Engineer"),
        ("user3@enterprise.org", "user3", "Priya Sharma (HR Director)", UserRole.END_USER, departments[4].id, "Director of People Operations"),
    ]
    users = []
    for email, uname, fname, role, dept_id, title in user_data:
        u = User(
            email=email,
            username=uname,
            full_name=fname,
            hashed_password=hashed_pwd,
            role=role,
            department_id=dept_id,
            job_title=title,
            is_active=True
        )
        db.add(u)
        users.append(u)
    db.flush()

    # 4. 10 Infrastructure Nodes
    infra_data = [
        ("Database-01", "Database", "10.0.4.12", "Production", HealthStatus.WARNING, 78.4, 82.1, 84.5, 450.2, 34.2, 99.95),
        ("Database-02-Replica", "Database", "10.0.4.13", "Production", HealthStatus.HEALTHY, 32.1, 44.5, 62.0, 180.0, 14.5, 99.99),
        ("K8s-Worker-Node-01", "Kubernetes Worker", "10.0.8.21", "Production", HealthStatus.HEALTHY, 45.0, 58.2, 40.1, 890.5, 8.2, 99.98),
        ("K8s-Worker-Node-02", "Kubernetes Worker", "10.0.8.22", "Production", HealthStatus.HEALTHY, 52.3, 61.4, 42.8, 920.1, 9.1, 99.98),
        ("API-Gateway-Edge-01", "API Gateway", "10.0.1.5", "Production", HealthStatus.HEALTHY, 28.5, 34.2, 22.0, 1450.0, 4.5, 100.0),
        ("Auth-SSO-Server-01", "App Server", "10.0.2.18", "Production", HealthStatus.HEALTHY, 38.0, 49.0, 31.5, 310.0, 12.0, 99.97),
        ("Enterprise-VPN-GW-01", "Router", "10.0.0.1", "Production", HealthStatus.HEALTHY, 41.2, 53.0, 28.0, 680.0, 16.8, 99.92),
        ("Redis-Session-Cluster-01", "Database", "10.0.5.10", "Production", HealthStatus.HEALTHY, 19.4, 68.0, 15.2, 780.0, 2.1, 99.99),
        ("Elasticsearch-Logging-01", "Server", "10.0.6.30", "Production", HealthStatus.HEALTHY, 64.2, 76.5, 71.0, 540.0, 22.4, 99.94),
        ("CI-CD-Jenkins-Runner-01", "Server", "10.0.9.50", "Staging", HealthStatus.HEALTHY, 22.0, 35.0, 45.0, 120.0, 15.0, 99.90)
    ]
    infra_nodes = []
    for host, ntype, ip, env, status, cpu, mem, disk, net, resp, upt in infra_data:
        node = InfrastructureNode(
            hostname=host,
            node_type=ntype,
            ip_address=ip,
            environment=env,
            status=status,
            cpu_usage=cpu,
            memory_usage=mem,
            disk_usage=disk,
            network_traffic_mbps=net,
            response_time_ms=resp,
            uptime_percentage=upt,
            last_ping=now
        )
        db.add(node)
        infra_nodes.append(node)
    db.flush()

    # 5. 20 IT Assets
    asset_data = [
        ("AST-5001", "PostgreSQL Primary Cluster (Database-01)", AssetType.DATABASE_SERVER, "SRV-PG-9901", "Rajesh Kumar", "Enterprise Database Systems", "Datacenter US-East-1", AssetStatus.ACTIVE, "10.0.4.12", "Linux Ubuntu 22.04 LTS", 64, 256, 4000),
        ("AST-5002", "PostgreSQL Standby Replica (Database-02)", AssetType.DATABASE_SERVER, "SRV-PG-9902", "Rajesh Kumar", "Enterprise Database Systems", "Datacenter US-East-1", AssetStatus.ACTIVE, "10.0.4.13", "Linux Ubuntu 22.04 LTS", 64, 256, 4000),
        ("AST-5003", "Kubernetes Production Master Node 01", AssetType.SERVER, "SRV-K8S-0101", "Sarah Connor", "Cloud Platform Engineering", "AWS us-east-1a", AssetStatus.ACTIVE, "10.0.8.10", "Red Hat Enterprise Linux 9", 32, 128, 1000),
        ("AST-5004", "Enterprise Core Switch Cisco Nexus 9000", AssetType.SWITCH, "SW-NX9K-4412", "Network Ops", "DevOps & Site Reliability", "Rack A-04", AssetStatus.ACTIVE, "10.0.0.2", "Cisco NX-OS 10.2", 8, 32, 256),
        ("AST-5005", "Palo Alto Next-Gen Perimeter Firewall", AssetType.ROUTER, "PA-5250-9988", "Chen Wei", "Cyber Security & SOC", "Rack A-01", AssetStatus.ACTIVE, "10.0.0.1", "PAN-OS 11.0", 16, 64, 512),
        ("AST-5006", "MacBook Pro 16 M3 Max (DevOps Lead)", AssetType.LAPTOP, "C02G894AM3M1", "Sarah Connor", "DevOps & Site Reliability", "Remote / Boston HQ", AssetStatus.ACTIVE, "192.168.1.104", "macOS Sonoma 14.5", 16, 64, 1000),
        ("AST-5007", "Dell Precision 5680 Workstation (DBA Lead)", AssetType.LAPTOP, "DELL-PR-7741", "Rajesh Kumar", "Enterprise Database Systems", "Austin Campus Floor 3", AssetStatus.ACTIVE, "192.168.2.88", "Windows 11 Pro Enterprise", 14, 32, 1000),
        ("AST-5008", "Lenovo ThinkPad P1 Gen 6 (Sec Lead)", AssetType.LAPTOP, "LEN-P1-3321", "Chen Wei", "Cyber Security & SOC", "Austin Campus Floor 2", AssetStatus.ACTIVE, "192.168.2.45", "Ubuntu Desktop 24.04", 14, 32, 1000),
        ("AST-5009", "Dell PowerEdge R750 VMware Hypervisor 01", AssetType.SERVER, "DEL-PE-8840", "Infrastructure Team", "DevOps & Site Reliability", "Datacenter US-East-1", AssetStatus.ACTIVE, "10.0.3.10", "VMware ESXi 8.0", 64, 512, 16000),
        ("AST-5010", "Dell PowerEdge R750 VMware Hypervisor 02", AssetType.SERVER, "DEL-PE-8841", "Infrastructure Team", "DevOps & Site Reliability", "Datacenter US-East-1", AssetStatus.ACTIVE, "10.0.3.11", "VMware ESXi 8.0", 64, 512, 16000),
        ("AST-5011", "HP Color LaserJet Enterprise MFP M681", AssetType.PRINTER, "HP-MFP-1092", "Office Admin", "Corporate IT Service Desk", "HQ Austin 3rd Floor East", AssetStatus.ACTIVE, "192.168.5.20", "HP FutureSmart Firmware", 2, 4, 32),
        ("AST-5012", "AWS Production Aurora RDS Cluster", AssetType.CLOUD_INSTANCE, "AWS-RDS-AURORA-PROD", "Sarah Connor", "Cloud Platform Engineering", "AWS Region us-east-1", AssetStatus.ACTIVE, "10.0.12.80", "AWS Managed Aurora", 32, 128, 5000),
        ("AST-5013", "Enterprise Okta Identity Provider Connector", AssetType.APPLICATION, "APP-OKTA-SSO-01", "Jordan Taylor", "Cyber Security & SOC", "Cloud SaaS", AssetStatus.ACTIVE, "10.0.2.18", "Enterprise SaaS", 4, 16, 100),
        ("AST-5014", "Corporate Jira Data Center Instance", AssetType.APPLICATION, "APP-JIRA-DC-01", "Marcus Vance", "DevOps & Site Reliability", "AWS us-east-1", AssetStatus.ACTIVE, "10.0.9.15", "Atlassian Jira 9.12", 16, 64, 500),
        ("AST-5015", "Jenkins Enterprise Master Controller", AssetType.SERVER, "SRV-JNK-MST-01", "Marcus Vance", "DevOps & Site Reliability", "AWS us-east-1", AssetStatus.ACTIVE, "10.0.9.50", "Linux Debian 12", 16, 64, 1000),
        ("AST-5016", "Docker Swarm Production Gateway 01", AssetType.SERVER, "SRV-DCK-SWM-01", "Sarah Connor", "DevOps & Site Reliability", "AWS us-east-1", AssetStatus.ACTIVE, "10.0.1.5", "Linux Ubuntu 22.04 LTS", 16, 32, 500),
        ("AST-5017", "Customer Portal Frontend Web Cluster", AssetType.APPLICATION, "APP-WEB-PORTAL-01", "David Kim", "Cloud Platform Engineering", "Kubernetes Pods", AssetStatus.ACTIVE, "10.0.8.21", "Node.js / React 18", 8, 16, 100),
        ("AST-5018", "Enterprise Payment Gateway Microservice", AssetType.APPLICATION, "APP-PAY-SRV-01", "Alex Morgan", "Cloud Platform Engineering", "Kubernetes Pods", AssetStatus.ACTIVE, "10.0.8.22", "Go 1.22 Runtime", 8, 16, 100),
        ("AST-5019", "Corporate Exchange Online Hybrid Connector", AssetType.APPLICATION, "APP-M365-EXCH-01", "Jordan Taylor", "Corporate IT Service Desk", "Microsoft 365 Cloud", AssetStatus.ACTIVE, "10.0.2.55", "Windows Server 2022", 8, 32, 200),
        ("AST-5020", "Global Edge Cloudflare CDN Tunnel", AssetType.ROUTER, "RTR-CF-EDGE-01", "Chen Wei", "DevOps & Site Reliability", "Anycast Edge", AssetStatus.ACTIVE, "172.64.80.1", "Cloudflare Warp OS", 8, 16, 100)
    ]
    assets = []
    for tag, name, atype, snum, owner, dept, loc, status, ip, os_name, cpu, ram, storage in asset_data:
        asset = Asset(
            asset_tag=tag,
            asset_name=name,
            asset_type=atype,
            serial_number=snum,
            owner=owner,
            department=dept,
            location=loc,
            status=status,
            ip_address=ip,
            operating_system=os_name,
            cpu_cores=cpu,
            ram_gb=ram,
            storage_gb=storage,
            purchase_date=now - timedelta(days=365),
            warranty_expiry=now + timedelta(days=365)
        )
        db.add(asset)
        assets.append(asset)
    db.flush()

    # 6. 20 Knowledge Articles
    kb_data = [
        ("KB-101", "VPN Connection Troubleshooting & Gateway Timeout", "Network",
         "Unable to connect to corporate VPN gateway or session drops every 5 minutes.",
         "Client indicates timeout waiting for TLS handshake, or MFA push notification not received.",
         "Stale local DNS cache, mismatched client tunnel MTU, or VPN gateway radius sync timeout.",
         "1. Check internet connectivity and ping 8.8.8.8.\n2. Flush local DNS via 'ipconfig /flushdns'.\n3. Verify MFA authenticator token time-sync in Okta/Duo.\n4. Reset VPN client network adapter profile.\n5. If issue persists, route through secondary European/US-West VPN gateway.",
         "vpn,network,anyconnect,openvpn,connectivity,dns"),
        
        ("KB-102", "PostgreSQL Database Connection Pool Exhaustion Resolution", "Database",
         "Applications report 'FATAL: remaining connection slots are reserved for non-replication superuser connections'.",
         "Database CPU rises above 85% and API endpoints return HTTP 500 error code with database pool timeout.",
         "Unclosed database connection leaks in backend microservices or sudden spike in traffic without PgBouncer scaling.",
         "1. Connect via superuser psql socket.\n2. Run: SELECT pid, now() - query_start AS duration, query, state FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC;\n3. Terminate idle-in-transaction connections: SELECT pg_terminate_backend(pid) WHERE state = 'idle in transaction';\n4. Increase max_connections in postgresql.conf and reload configuration: SELECT pg_reload_conf();\n5. Adjust connection pool pool_size and max_overflow in backend SQLAlchemy settings.",
         "database,postgres,sql,connection pool,pgbouncer,deadlock,cpu"),
        
        ("KB-103", "SSO & SAML Authentication Token Validation Failures", "Authentication",
         "Users receiving '401 Unauthorized' or infinite redirect loop on enterprise SSO login.",
         "Login page redirects back to login without session cookies set, or error 'invalid_token'.",
         "Identity Provider SAML/OIDC signing certificate expiration, system clock skew > 5 minutes, or Redis session store cluster failure.",
         "1. Check IdP tenant status at status.okta.com / Azure AD health.\n2. Verify NTP clock synchronization on SSO gateway servers: ntpdate -q pool.ntp.org.\n3. Validate SAML token expiration timestamp in decoded JWT payload.\n4. Flush invalid session tokens in Redis session cache: redis-cli KEYS 'sess:*' | xargs redis-cli DEL.\n5. Restart the authentication microservice container cluster.",
         "sso,saml,jwt,auth,okta,oauth,login,password"),

        ("KB-104", "High CPU & Memory Spike on Linux Database Servers", "Infrastructure",
         "Server CPU usage exceeds 90% threshold for > 5 consecutive minutes.",
         "Alert ALT-9001 triggered; slow query response times > 500ms.",
         "Missing database table index on hot audit/history tables or unbounded full table scans.",
         "1. Inspect top processes with 'htop' or 'pidstat -u 2 5'.\n2. Run 'EXPLAIN ANALYZE' on top queries in pg_stat_statements.\n3. Add concurrent index on high cardinality filter columns: CREATE INDEX CONCURRENTLY idx_name ON table(col);\n4. Clean up disk WAL files and verify memory swap activity.\n5. Deploy configuration hotfix via Jenkins CI/CD pipeline.",
         "cpu,infrastructure,database,load,server,memory,incident-1025"),

        ("KB-105", "Email Delivery Failures & Exchange Online Quota Issues", "Email",
         "Outbound or internal emails queued and delayed by over 30 minutes.",
         "Users receive NDR error '550 5.7.1 Service unavailable' or mail flow rules blocked.",
         "Microsoft 365 Exchange connector throttling or DNS MX / SPF record lookup failure.",
         "1. Check Microsoft 365 Service Health Dashboard for Exchange Online incidents.\n2. Verify domain MX and TXT SPF records using 'dig txt yourdomain.com'.\n3. Review Exchange Admin Center Mail Flow Message Trace logs.\n4. Release quarantined valid transactional messages in Security Admin Center.\n5. Restart local mail submission gateway spoolers.",
         "email,outlook,exchange,smtp,office365,ndr"),

        ("KB-106", "Kubernetes Pod CrashLoopBackOff Diagnostic Runbook", "Cloud",
         "Application microservice pod repeatedly crashing and restarting.",
         "Pod status shows CrashLoopBackOff or OOMKilled with exit code 137.",
         "Out of Memory (OOM) killing due to tight container memory limits, or missing required environment variables/secrets.",
         "1. Inspect pod events: kubectl describe pod <pod_name> -n production.\n2. Review container termination reason and logs: kubectl logs <pod_name> --previous.\n3. If exit code 137, increase container memory limits in Helm values.yaml.\n4. Verify Kubernetes secrets and configmaps are mounted correctly.\n5. Trigger rolling restart: kubectl rollout restart deployment/<deployment_name>.",
         "kubernetes,k8s,cloud,docker,crashloop,oom,pod"),

        ("KB-107", "Ransomware Endpoint Isolation & Quarantine Protocol", "Security",
         "Unusual file encryption activity or malicious PowerShell process detected on endpoint.",
         "EDR (CrowdStrike / Defender) triggers High severity alert on user workstation.",
         "Execution of phishing email attachment containing malicious payload.",
         "1. Immediately trigger network containment via EDR console.\n2. Revoke active Active Directory and Okta user credentials.\n3. Kill suspicious processes and capture forensic volatile memory image.\n4. Re-image endpoint workstation to clean corporate golden master image.\n5. Restore user OneDrive/SharePoint files from point-in-time backup.",
         "security,ransomware,malware,soc,quarantine,edr,phishing"),

        ("KB-108", "Jira & GitHub Webhook Synchronization Troubleshooting", "Software",
         "ITSM Incidents not creating linked Jira tickets or GitHub PR status not updating.",
         "Jira issue link remains in 'Pending Sync' status with HTTP 403 / 404 error.",
         "Invalid Jira API token, mismatched Jira issue type permissions, or webhook IP filtering.",
         "1. Verify Jira API token validity in Application Settings / .env.\n2. Confirm ITSM service account has 'Create Issues' and 'Assign Issues' permission in Jira Project.\n3. Check Jira project issue types (Bug, Task, Incident) match configuration.\n4. Test webhook connectivity with: curl -I -u email:token https://your-domain.atlassian.net/rest/api/2/myself.\n5. Trigger manual sync from the ITSM Incident Detail page.",
         "jira,github,devops,sync,webhook,integration"),

        ("KB-109", "PostgreSQL Deadlock Detection & Resolution", "Database",
         "Transactions failing with 'deadlock detected: Process waiting for ShareLock'.",
         "Multiple concurrent workers attempting to update overlapping foreign key tables.",
         "Inconsistent ordering of row locks across concurrent application threads.",
         "1. Check postgres error log for deadlock statement graphs.\n2. Inspect lock conflicts: SELECT * FROM pg_locks WHERE NOT granted;\n3. Refactor application database queries to sort IDs before executing batch UPDATE/DELETE.\n4. Use SELECT ... FOR UPDATE SKIP LOCKED for worker queue consumers.\n5. Ensure appropriate transactions have short timeouts: SET lock_timeout = '5s';",
         "database,postgres,deadlock,lock,query,sql"),

        ("KB-110", "Docker Container Health Check Failure Recovery", "Infrastructure",
         "Docker container status reporting (unhealthy) and traffic being dropped.",
         "Docker daemon restart loops or health probe curl failing with exit code 1.",
         "Internal application port hung, health check endpoint returning 503, or full disk space on /var/lib/docker.",
         "1. Inspect docker container health log: docker inspect --format='{{json .State.Health}}' <container_id>.\n2. Check host disk space: df -h /var/lib/docker.\n3. Clean unused containers and dangling images: docker system prune -f.\n4. Check container stdout logs: docker logs --tail 100 <container_id>.\n5. Restart unhealthy service container: docker restart <container_id>.",
         "docker,container,health,infrastructure,devops"),

        ("KB-111", "Wi-Fi 6 Enterprise 802.1X Authentication Troubleshooting", "Network",
         "Employees unable to connect to corporate 'Enterprise-Secure' SSID.",
         "Client prompts for password repeatedly or reports 'Can't connect to this network'.",
         "Expired RADIUS server TLS certificate or missing intermediate root CA on client OS.",
         "1. Install corporate Root CA certificate via MDM.\n2. Forget the Wi-Fi network and reconnect selecting WPA2/WPA3-Enterprise.\n3. Verify RADIUS server status in Network Operations Center.\n4. Check client MAC address filtering blacklist in wireless controller.",
         "wifi,network,radius,802.1x,wireless"),

        ("KB-112", "Jenkins CI/CD Build Pipeline Failure Diagnostics", "Software",
         "Automated deployment pipeline fails at 'Backend Tests' or 'Docker Build' stage.",
         "Build status turns RED with non-zero exit code in console log.",
         "Unit test assertion failure, broken dependency package, or Docker build cache corruption.",
         "1. Open Jenkins build console output and search for 'FAILED' / 'Error'.\n2. Run failing unit test locally in reproduction environment.\n3. If dependency issue, verify requirements.txt / package-lock.json sha checksums.\n4. Clear Jenkins workspace directory and re-trigger build with clean cache.\n5. Confirm Docker daemon running on Jenkins agent runner.",
         "jenkins,cicd,pipeline,devops,build,docker"),

        ("KB-113", "Corporate Laptop BitLocker / FileVault Recovery", "Hardware",
         "User prompted for 48-digit BitLocker recovery key upon boot.",
         "Blue screen 'BitLocker recovery' after firmware/BIOS update or motherboard change.",
         "TPM chip PCR measurement changes following UEFI/BIOS security update.",
         "1. Service Desk Agent looks up user's BitLocker key in Microsoft Entra ID / Intune portal.\n2. Have user input 48-digit key on recovery screen.\n3. Once logged in, open PowerShell as Admin: Suspend-BitLocker -MountPoint 'C:' -RebootCount 1.\n4. Restart machine to let TPM re-seal platform measurements.",
         "hardware,bitlocker,laptop,security,tpm,windows"),

        ("KB-114", "Cloudflare CDN Edge Cache Purge & SSL Handshake Fix", "Cloud",
         "Static assets returning stale JavaScript bundles or SSL handshake error 525.",
         "Users seeing broken UI layout after production release deployment.",
         "Cloudflare CDN edge cache serving pre-release bundle or origin server TLS cert mismatch.",
         "1. Execute Cloudflare API cache purge: POST /zones/:id/purge_cache with purge_everything: true.\n2. Check origin server SSL certificate validity with: openssl s_client -connect origin:443.\n3. Ensure SSL/TLS encryption mode in Cloudflare dashboard is set to 'Full (Strict)'.\n4. Verify cache headers in origin Nginx configuration: Cache-Control: no-cache, must-revalidate.",
         "cloudflare,cdn,cloud,cache,ssl,frontend"),

        ("KB-115", "Redis Distributed Cache Out-Of-Memory (OOM) Eviction", "Infrastructure",
         "Redis write operations failing with 'OOM command not allowed when used memory > maxmemory'.",
         "Application latency spikes from 10ms to 450ms as cache falls back to cold database queries.",
         "Keys created without TTL expiration or maxmemory-policy set to 'noeviction'.",
         "1. Connect via redis-cli: INFO memory.\n2. Identify big keys: redis-cli --bigkeys.\n3. Change eviction policy dynamically: CONFIG SET maxmemory-policy allkeys-lru.\n4. Set missing TTL on runaway cache prefixes: SCAN and EXPIRE.\n5. Scale Redis node cluster RAM memory capacity.",
         "redis,cache,infrastructure,memory,database"),

        ("KB-116", "Slack & Microsoft Teams Webhook Alert Integration Fix", "Software",
         "Ops channel not receiving automated incident notifications.",
         "Incoming webhook returning HTTP 404 (Channel archived) or HTTP 400 (Invalid payload).",
         "Deleted incoming webhook URL or JSON schema mismatch in webhook payload.",
         "1. Re-generate Incoming Webhook in Slack App Directory / Teams Workflow.\n2. Update WEBHOOK_URL in ITSM System Settings.\n3. Test notification dispatcher with sample test event.\n4. Verify channel permissions allow external bot postings.",
         "slack,teams,webhook,notifications,software"),

        ("KB-117", "PostgreSQL WAL Disk Full Recovery", "Database",
         "PostgreSQL service stopped unexpectedly; log indicates 'No space left on device'.",
         "Server root/data partition at 100% disk usage due to pg_wal archive accumulation.",
         "Stale replication slot preventing PostgreSQL from removing archived WAL segments.",
         "1. Identify active replication slots: SELECT slot_name, active, pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) FROM pg_replication_slots;\n2. Drop orphaned inactive slot: SELECT pg_drop_replication_slot('orphaned_slot_name');\n3. DO NOT delete WAL files manually with rm - use pg_archivecleanup.\n4. Restart PostgreSQL service and verify disk recovery: df -h.\n5. Expand EBS / cloud disk volume by 100GB to provide safety headroom.",
         "database,postgres,disk,wal,storage,infrastructure"),

        ("KB-118", "OAuth 2.0 Client Secret Rotation & Zero-Downtime Rollout", "Authentication",
         "Third-party API integrations failing with 'invalid_client'.",
         "Automated background jobs failing to refresh OAuth tokens.",
         "Expired client secret after 180-day security rotation compliance policy.",
         "1. In IdP / App registration portal, generate secondary client secret before expiring primary.\n2. Update application secret manager (AWS Secrets Manager / Vault).\n3. Trigger rolling restart of backend microservices.\n4. Verify successful token generation: POST /oauth/v2/token.\n5. Delete old expired client secret from identity provider.",
         "oauth,auth,security,token,secret"),

        ("KB-119", "Nginx Reverse Proxy 502 Bad Gateway Diagnostics", "Application",
         "End users receive '502 Bad Gateway' when accessing ITSM web portal.",
         "Nginx error log shows 'connect() failed (111: Connection refused) while connecting to upstream'.",
         "Backend FastAPI / Python uvicorn process crashed or listening on wrong local unix socket / port.",
         "1. Check backend process status: systemctl status itsm-backend or docker ps.\n2. Inspect backend error traceback: journalctl -u itsm-backend -n 50 --no-pager.\n3. Verify backend listening on 127.0.0.1:8000: netstat -tlpn | grep 8000.\n4. Restart backend daemon: systemctl restart itsm-backend.\n5. Test curl -I http://127.0.0.1:8000/api/health.",
         "nginx,502,proxy,application,gateway,fastapi"),

        ("KB-120", "Hardware Monitor & Docking Station Dual Display Blanking", "Hardware",
         "External dual 4K monitors plugged into Thunderbolt 4 dock not receiving video signal.",
         "Monitors go to sleep immediately; laptop charging works but displays remain black.",
         "Thunderbolt security authorization disabled or DisplayLink graphics driver mismatch.",
         "1. Power-cycle the docking station by unplugging AC power for 30 seconds.\n2. Update Thunderbolt 4 firmware and DisplayLink driver to latest release.\n3. Enable 'Thunderbolt PCIe tunneling' in laptop UEFI BIOS.\n4. Test with alternate certified 40Gbps Thunderbolt cable.",
         "hardware,monitor,dock,display,laptop")
    ]
    for num, title, cat, prob, symp, cause, res, tags in kb_data:
        db.add(KnowledgeArticle(
            article_number=num,
            title=title,
            category=cat,
            problem_summary=prob,
            symptoms=symp,
            cause=cause,
            resolution=res,
            tags=tags,
            views_count=142,
            helpful_count=38
        ))
    db.flush()

    # 7. 30 Realistic Incidents (Including the Critical Database Failure INC-1025)
    incident_seeds = [
        # (Incident Number, Title, Description, Category, Impact, Urgency, Priority, Status, ReporterIdx, TechIdx, DeptIdx, Service, AssetIdx, JiraKey, JiraStatus)
        ("INC-1001", "Database Server CPU Exceeded 90% (Database-01)",
         "Database-01 CPU exceeded 90% threshold for 5 consecutive minutes. Query contention on transaction history.",
         "Database", "High", "High", IncidentPriority.P1, IncidentStatus.IN_PROGRESS, 0, 3, 2, "Core DB Cluster", 0, "ITSM-245", "In Progress"),
        
        ("INC-1002", "SSO Login Token Expiration Failure for Remote Workers",
         "Remote workers reporting 401 Unauthorized errors during Okta SAML login flow.",
         "Authentication", "High", "Medium", IncidentPriority.P2, IncidentStatus.RESOLVED, 7, 5, 1, "Identity Provider", 12, "ITSM-246", "Done"),

        ("INC-1003", "Corporate VPN Gateway US-East Tunnel Intermittent Latency",
         "Employees in Boston HQ experiencing VPN disconnects every 15 minutes. Packet loss at 18%.",
         "Network", "High", "Medium", IncidentPriority.P2, IncidentStatus.IN_PROGRESS, 8, 2, 0, "Enterprise VPN", 4, "ITSM-247", "In Progress"),

        ("INC-1004", "Microsoft Exchange Hybrid Mail Connector Rate Limiting",
         "Outbound customer invoice emails delayed by 45 minutes. Exchange mail flow queue backed up.",
         "Email", "Medium", "High", IncidentPriority.P2, IncidentStatus.RESOLVED, 9, 5, 4, "Exchange Online", 18, None, None),

        ("INC-1005", "Kubernetes Production Worker Node 02 Memory Pressure",
         "K8s worker node reported MemoryPressure condition. 2 pods evicted to standby node.",
         "Cloud", "Medium", "Medium", IncidentPriority.P3, IncidentStatus.RESOLVED, 0, 2, 3, "K8s Production Cluster", 2, None, None),

        ("INC-1006", "Ransomware Behavioral Quarantine on Finance Endpoint",
         "CrowdStrike EDR isolated finance analyst workstation following suspicious encoded PowerShell execution.",
         "Security", "High", "High", IncidentPriority.P1, IncidentStatus.RESOLVED, 4, 4, 1, "Endpoint Security", 7, "ITSM-248", "Done"),

        ("INC-1007", "Database Connection Pool Exhaustion on Customer Portal",
         "Backend API returning 500 Internal Server Error due to pool timeout waiting for connection.",
         "Database", "High", "High", IncidentPriority.P1, IncidentStatus.RESOLVED, 8, 3, 2, "Customer Portal DB", 0, "ITSM-249", "Done"),

        ("INC-1008", "MacBook Pro M3 Screen Flickering and Thunderbolt Failure",
         "Senior Engineer reporting external monitor flickering and charging drops on Thunderbolt port 1.",
         "Hardware", "Low", "Medium", IncidentPriority.P4, IncidentStatus.NEW, 7, 5, 4, "Endpoint Hardware", 5, None, None),

        ("INC-1009", "Customer Checkout Microservice HTTP 504 Gateway Timeouts",
         "Spike in payment transaction response times > 3500ms causing payment gateway timeouts.",
         "Application", "High", "High", IncidentPriority.P1, IncidentStatus.IN_PROGRESS, 1, 6, 3, "Payment Service", 17, "ITSM-250", "In Progress"),

        ("INC-1010", "Jenkins CI/CD Worker Node Disk Space at 94%",
         "CI runner unable to cache Docker build layers due to disk space shortage on /var/lib/docker.",
         "Infrastructure", "Medium", "High", IncidentPriority.P2, IncidentStatus.RESOLVED, 2, 2, 0, "CI/CD Pipeline", 14, None, None),

        ("INC-1011", "Wi-Fi 6 Enterprise Authentication Failure in Austin Office Floor 3",
         "Laptops unable to connect to corporate 802.1X Wi-Fi network after RADIUS certificate renewal.",
         "Network", "Medium", "Medium", IncidentPriority.P3, IncidentStatus.RESOLVED, 9, 5, 4, "Corporate Wi-Fi", 3, None, None),

        ("INC-1012", "PostgreSQL Deadlock Storm During Bulk Nightly Reconciliation",
         "Nightly financial ledger batch job failed with deadlock detected across table partitions.",
         "Database", "High", "Medium", IncidentPriority.P2, IncidentStatus.RESOLVED, 3, 3, 2, "Data Warehouse DB", 1, None, None),

        ("INC-1013", "Slack Webhook Notifications Failing for Critical Alerts",
         "Alerts generated by Prometheus not routing to #ops-incident-war-room Slack channel.",
         "Software", "Low", "Medium", IncidentPriority.P4, IncidentStatus.CLOSED, 0, 5, 0, "Notification Service", 13, None, None),

        ("INC-1014", "Docker Swarm Production Gateway High Memory Utilization",
         "Edge ingress gateway memory usage exceeded 85%. Traffic re-routed to backup gateway.",
         "Infrastructure", "High", "Medium", IncidentPriority.P2, IncidentStatus.IN_PROGRESS, 2, 2, 0, "Edge Gateway", 15, None, None),

        ("INC-1015", "Expired Wildcard SSL Certificate on Internal Staging Subdomains",
         "Developers encountering security certificate warnings on *.dev.internal.enterprise.org.",
         "Security", "Medium", "Low", IncidentPriority.P4, IncidentStatus.RESOLVED, 8, 4, 1, "Internal DNS & SSL", 19, None, None),

        ("INC-1016", "Cloudflare CDN Edge Cache Serving Stale React Bundle",
         "Users experiencing white screen after v2.4.1 release due to missing chunk hashes.",
         "Cloud", "High", "High", IncidentPriority.P1, IncidentStatus.RESOLVED, 8, 6, 3, "Web Application", 16, None, None),

        ("INC-1017", "HP LaserJet 3rd Floor Paper Jam & Network Spooler Lock",
         "Print queue locked with 45 pending documents. Printer unresponsive on network IP.",
         "Hardware", "Low", "Low", IncidentPriority.P4, IncidentStatus.CLOSED, 9, 5, 4, "Office Printing", 10, None, None),

        ("INC-1018", "Redis Distributed Cache Node 01 Eviction Rate Anomaly",
         "Redis cache memory maxed at 98% with high eviction rate slowing product search queries.",
         "Database", "Medium", "High", IncidentPriority.P2, IncidentStatus.IN_PROGRESS, 2, 3, 2, "Redis Cluster", 7, None, None),

        ("INC-1019", "Active Directory Password Sync Delay Between Regions",
         "New user password resets in London office taking over 2 hours to replicate to Austin domain controllers.",
         "Authentication", "Medium", "Medium", IncidentPriority.P3, IncidentStatus.ASSIGNED, 7, 5, 1, "Active Directory", 12, None, None),

        ("INC-1020", "Palo Alto Firewall Core CPU Spike Following Rule Base Update",
         "Core firewall packet inspection latency increased by 120ms following threat prevention rule update.",
         "Network", "High", "High", IncidentPriority.P1, IncidentStatus.RESOLVED, 4, 4, 1, "Core Perimeter Firewall", 4, "ITSM-251", "Done"),

        ("INC-1021", "Developer Sandbox AWS IAM Permission Denied for S3 Bucket",
         "Engineering team cannot upload deployment artifacts to release bucket.",
         "Cloud", "Low", "Medium", IncidentPriority.P4, IncidentStatus.RESOLVED, 8, 6, 3, "AWS Cloud Services", 11, None, None),

        ("INC-1022", "Corporate Zoom Room AV System Black Screen in Boardroom",
         "Boardroom Zoom Room TV display showing no input signal ahead of executive meeting.",
         "Hardware", "High", "High", IncidentPriority.P1, IncidentStatus.RESOLVED, 1, 5, 4, "AV Conference Systems", 10, None, None),

        ("INC-1023", "Nginx Ingress 502 Bad Gateway on Customer Support Portal",
         "Support portal API container crashed with uncaught promise rejection in authentication middleware.",
         "Application", "High", "Medium", IncidentPriority.P2, IncidentStatus.RESOLVED, 7, 6, 3, "Customer Portal", 16, None, None),

        ("INC-1024", "Elasticsearch Logging Cluster Red Health Status",
         "Unassigned shards on logging cluster due to disk watermark threshold breach on node 3.",
         "Infrastructure", "High", "Medium", IncidentPriority.P2, IncidentStatus.ASSIGNED, 2, 2, 0, "Log Aggregation", 8, None, None),

        # INC-1025: Key Scenario Incident
        ("INC-1025", "Critical Database Server CPU Exceeded 90% (Database-01)",
         "Database Server CPU exceeded 90% for 5 consecutive minutes. Query contention and lock bottleneck on incident_history table.",
         "Infrastructure", "High", "High", IncidentPriority.P1, IncidentStatus.NEW, 0, 2, 2, "Database-01 Subsystem", 0, "ITSM-245", "In Progress"),

        ("INC-1026", "Corporate Jira Webhook Sync Timeout for Emergency Changes",
         "Change requests not syncing status back to Jira service desk project.",
         "Software", "Low", "Medium", IncidentPriority.P4, IncidentStatus.NEW, 1, 5, 0, "ITSM Jira Integration", 13, None, None),

        ("INC-1027", "OAuth 2.0 Client Secret Expiration on Billing Connector",
         "Billing batch job failed authentication against Stripe enterprise sync webhook.",
         "Authentication", "High", "High", IncidentPriority.P1, IncidentStatus.RESOLVED, 7, 4, 1, "Billing Gateway", 17, None, None),

        ("INC-1028", "Dell PowerEdge Hypervisor 02 Fan Failure Warning",
         "IPMI hardware sensor reported fan module 3 speed below critical threshold (1100 RPM).",
         "Hardware", "Medium", "Low", IncidentPriority.P3, IncidentStatus.ASSIGNED, 0, 2, 0, "Hypervisor Cluster", 9, None, None),

        ("INC-1029", "Enterprise Email Phishing Campaign Targeted at HR Dept",
         "14 HR employees received spoofed payroll verification emails with credential harvesting link.",
         "Security", "High", "High", IncidentPriority.P1, IncidentStatus.IN_PROGRESS, 9, 4, 1, "Email Gateway & EDR", 18, "ITSM-252", "In Progress"),

        ("INC-1030", "Customer Portal Search Query Response Degradation",
         "Search API response times degraded from 45ms to 1200ms due to unoptimized regex query.",
         "Application", "Medium", "Medium", IncidentPriority.P3, IncidentStatus.NEW, 8, 6, 3, "Customer Portal", 16, None, None)
    ]

    incidents = []
    for inc_num, title, desc, cat, imp, urg, prio, status, rep_idx, tech_idx, dept_idx, service, asset_idx, jkey, jstatus in incident_seeds:
        resp_due, res_due = calculate_sla_deadlines(prio, now - timedelta(hours=2))
        
        inc = Incident(
            incident_number=inc_num,
            title=title,
            description=desc,
            category=cat,
            impact=imp,
            urgency=urg,
            priority=prio,
            status=status,
            reporter_id=users[rep_idx].id,
            assigned_technician_id=users[tech_idx].id if tech_idx is not None else None,
            department_id=departments[dept_idx].id if dept_idx is not None else None,
            affected_service=service,
            asset_id=assets[asset_idx].id if asset_idx is not None else None,
            sla_response_due=resp_due,
            sla_resolution_due=res_due,
            responded_at=now - timedelta(hours=1, minutes=45) if status != IncidentStatus.NEW else None,
            resolved_at=now - timedelta(minutes=30) if status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED] else None,
            closed_at=now - timedelta(minutes=10) if status == IncidentStatus.CLOSED else None,
            ai_probable_cause="Resource starvation or blocking transactions causing service degradation.",
            ai_recommendations="1. Inspect telemetry logs.\n2. Terminate blocking lock PID sessions.\n3. Deploy hotfix via CI/CD.",
            ai_confidence=94.5,
            ai_suggested_kb_ids="KB-102, KB-104",
            ai_similar_incidents="INC-1001, INC-1007",
            resolution_notes="Optimized queries, killed deadlock sessions, and validated recovery." if status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED] else None,
            root_cause="Unindexed query storm on transactional tables." if status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED] else None,
            jira_issue_key=jkey,
            jira_sync_status="In Sync" if jkey else "Not Linked",
            jira_issue_url=f"https://company-itsm.atlassian.net/browse/{jkey}" if jkey else None,
            created_at=now - timedelta(hours=3),
            updated_at=now - timedelta(minutes=15)
        )
        db.add(inc)
        incidents.append(inc)
    db.flush()

    # 8. 10 Service Requests
    req_seeds = [
        ("REQ-2001", "Developer AWS Sandbox Account Provisioning", "New user account", "Provision AWS development account with limited billing budget of $500/month.", "Medium", ServiceRequestStatus.APPROVED, 8, "Jordan Taylor"),
        ("REQ-2002", "Hardware Upgrade to 64GB RAM for SRE Workstation", "Hardware request", "Request additional 32GB RAM module for local Kubernetes load testing.", "Medium", ServiceRequestStatus.IN_PROGRESS, 2, "Maya Lin"),
        ("REQ-2003", "Corporate GlobalProtect VPN Access for Contractor", "VPN access", "Grant 90-day time-limited VPN profile for external security auditor.", "High", ServiceRequestStatus.APPROVED, 4, "Jordan Taylor"),
        ("REQ-2004", "Docker Desktop Enterprise License Renewal", "Software installation", "Request enterprise Docker Desktop seat license for mobile development team.", "Low", ServiceRequestStatus.COMPLETED, 8, "Jordan Taylor"),
        ("REQ-2005", "Emergency Production Database Read-Only Access", "System access", "Temporary read-only credentials for customer incident investigation.", "High", ServiceRequestStatus.APPROVED, 3, "Sarah Connor"),
        ("REQ-2006", "New Employee Laptop Provisioning (MacBook Pro 16 M3)", "Laptop request", "Standard engineering onboarding hardware bundle with 4K external display.", "Medium", ServiceRequestStatus.IN_PROGRESS, 9, "Maya Lin"),
        ("REQ-2007", "Okta MFA Reset Following Device Replacement", "Password reset", "User replaced smartphone; needs Okta Verify MFA registration code reset.", "High", ServiceRequestStatus.COMPLETED, 7, "Jordan Taylor"),
        ("REQ-2008", "Shared Mailbox Creation for Customer SRE Escalations", "Email access", "Create sre-escalations@enterprise.org shared mailbox with 5 delegates.", "Low", ServiceRequestStatus.COMPLETED, 1, "Jordan Taylor"),
        ("REQ-2009", "JetBrains All Products Pack License Allocation", "Software installation", "Allocate JetBrains IDE license for newly joined backend engineer.", "Low", ServiceRequestStatus.SUBMITTED, 8, None),
        ("REQ-2010", "Static Public IP Allocation for Edge BGP Peer", "System access", "Allocate static IP /29 block for redundant internet circuit.", "High", ServiceRequestStatus.PENDING_APPROVAL, 0, "Marcus Vance")
    ]
    for rnum, title, rtype, desc, urg, status, req_idx, assigned in req_seeds:
        db.add(ServiceRequest(
            request_number=rnum,
            title=title,
            request_type=rtype,
            description=desc,
            urgency=urg,
            status=status,
            requester_id=users[req_idx].id,
            assigned_to=assigned,
            approval_required=True,
            approver_name="Elena Rostova (IT Manager)",
            approval_notes="Approved in accordance with enterprise IT security policy.",
            sla_due=now + timedelta(hours=8),
            completed_at=now - timedelta(hours=1) if status == ServiceRequestStatus.COMPLETED else None,
            created_at=now - timedelta(days=1)
        ))
    db.flush()

    # 9. 5 Problems
    prb_seeds = [
        ("PRB-3001", "PostgreSQL Connection Starvation Under Concurrent Traffic Spikes", "Database", ProblemStatus.UNDER_INVESTIGATION, "High",
         "Memory leak in legacy microservice connection pooler holding idle sessions indefinitely.",
         "Restart connection pooler every 6 hours and kill idle transactions.",
         "Refactor backend application to use scoped SQLAlchemy session lifecycle and deploy PgBouncer connection pool proxy.",
         "Enterprise Database Systems"),
        
        ("PRB-3002", "Okta SAML Token Clock Skew on Virtualized Gateways", "Authentication", ProblemStatus.KNOWN_ERROR, "Medium",
         "NTP daemon drift on ESXi virtual hosts causing token validation rejection for remote clients.",
         "Resynchronize VM guest clock with host hardware RTC.",
         "Enforce precision PTP time protocol across all hypervisor hosts and relax SAML validation clock skew tolerance to 120s.",
         "Cyber Security & SOC"),

        ("PRB-3003", "Kubernetes Ingress Gateway Memory Leaks Under WebSocket Load", "Cloud", ProblemStatus.WORKAROUND_FOUND, "High",
         "Nginx Ingress controller buffer retention bug with long-lived WebSocket connections.",
         "Automated rolling restart of ingress pod replicas every midnight.",
         "Upgrade ingress-nginx helm chart to version 1.10.1 with memory buffer leak patch.",
         "Cloud Platform Engineering"),

        ("PRB-3004", "BGP Route Flapping on Primary Fiber Uplink", "Network", ProblemStatus.RESOLVED, "High",
         "Faulty SFP+ optical transceiver on core boundary edge router.",
         "Traffic diverted through secondary backup 10Gbps transit provider.",
         "Replaced defective SFP+ module and cleaned optical fiber patch cable connector.",
         "DevOps & Site Reliability"),

        ("PRB-3005", "CI/CD Jenkins Docker Daemon Socket Lock Contention", "Infrastructure", ProblemStatus.LOGGED, "Medium",
         "Concurrent parallel builds overloading Docker daemon unix socket with build cache builds.",
         "Limit concurrent executor jobs to 4 per runner.",
         "Migrate Jenkins build executors to ephemeral Kubernetes pod agents using Kaniko for rootless Docker builds.",
         "DevOps & Site Reliability")
    ]
    for pnum, title, cat, status, imp, root, workaround, perm, team in prb_seeds:
        prb = Problem(
            problem_number=pnum,
            title=title,
            description=f"Root cause investigation for recurring {cat} anomalies.",
            category=cat,
            status=status,
            impact=imp,
            root_cause=root,
            workaround=workaround,
            permanent_solution=perm,
            assigned_team=team,
            created_at=now - timedelta(days=5)
        )
        db.add(prb)
    db.flush()

    # Link incidents to problem 1
    p1 = db.query(Problem).filter(Problem.problem_number == "PRB-3001").first()
    if p1:
        related_incidents = db.query(Incident).filter(Incident.incident_number.in_(["INC-1001", "INC-1007", "INC-1025"])).all()
        p1.incidents.extend(related_incidents)

    # 10. 5 Changes (RFCs)
    chg_seeds = [
        ("CHG-4001", "Deploy Partial B-Tree Index and Connection Pool Optimization on Database-01", ChangeType.NORMAL, ChangeStatus.COMPLETED,
         "Sarah Connor (Senior SRE)", "Enterprise Database Systems",
         "Apply partial index on incident_history(incident_id, timestamp) and reconfigure PgBouncer connection limits to eliminate CPU contention.",
         "Resolve recurring P1 database spikes (INC-1001, INC-1025).",
         "Medium", "High",
         "1. Backup database snapshot.\n2. Execute CREATE INDEX CONCURRENTLY.\n3. Reload PgBouncer config.\n4. Run health check verification.",
         "1. DROP INDEX CONCURRENTLY idx_incident_history_perf;\n2. Revert PgBouncer config to previous revision.",
         "Execute 10,000 synthetic queries and verify P99 latency < 25ms.",
         now - timedelta(hours=2), now - timedelta(hours=1), "Elena Rostova (IT Manager)", now - timedelta(hours=3)),

        ("CHG-4002", "Upgrade Kubernetes Production Master Nodes to v1.30.2", ChangeType.STANDARD, ChangeStatus.SCHEDULED,
         "Alex Rivera (Cloud Ops)", "Cloud Platform Engineering",
         "Rolling upgrade of Kubernetes control plane components and worker node AMI images.",
         "Quarterly platform security compliance and performance enhancements.",
         "Medium", "High",
         "Execute kubeadm upgrade plan and cordon/drain worker nodes sequentially.",
         "Restore control plane from etcd snapshot backup taken at T-10min.",
         "Run Sonobuoy conformance test suite and verify pod ingress routes.",
         now + timedelta(days=2), now + timedelta(days=2, hours=4), "Elena Rostova (IT Manager)", now - timedelta(days=1)),

        ("CHG-4003", "Emergency Firewall Rule Update for Zero-Day Threat Mitigation", ChangeType.EMERGENCY, ChangeStatus.COMPLETED,
         "Chen Wei (SOC Lead)", "Cyber Security & SOC",
         "Block inbound malicious IP range 198.51.100.0/24 targeting CVE-2024-4412 SSL VPN vulnerability.",
         "Active threat intelligence advisory from CISA regarding targeted exploitation attempts.",
         "Critical", "Critical",
         "Push emergency drop policy to Palo Alto perimeter firewalls via Panorama template.",
         "Disable firewall rule policy ID 9942 if legitimate business traffic is impacted.",
         "Verify dropped connection counters on firewall dashboard.",
         now - timedelta(days=1, hours=4), now - timedelta(days=1, hours=3), "Marcus Vance (Global Admin)", now - timedelta(days=1, hours=5)),

        ("CHG-4004", "Migrate Corporate Email Relays to Microsoft 365 Direct Send", ChangeType.NORMAL, ChangeStatus.APPROVAL,
         "Jordan Taylor (IT Support)", "Corporate IT Service Desk",
         "Decommission legacy on-premise SMTP relay servers and route all app notifications through Exchange Online direct send.",
         "Reduce on-premise server maintenance overhead and improve email deliverability.",
         "Low", "Medium",
         "Update SPF TXT records, configure TLS connector in M365 Admin Center, update app smtp settings.",
         "Re-enable DNS records pointing to on-premise relay cluster.",
         "Send test notification batches across 5 departments.",
         now + timedelta(days=4), now + timedelta(days=4, hours=2), None, None),

        ("CHG-4005", "Automated Database Snapshot Retention Policy Rollout", ChangeType.STANDARD, ChangeStatus.IMPLEMENTATION,
         "Rajesh Kumar (Principal DBA)", "Enterprise Database Systems",
         "Implement AWS Backup policy for automated 15-minute point-in-time recovery and cross-region replication.",
         "Comply with ISO 27001 disaster recovery RPO requirements (RPO < 15min).",
         "Low", "Medium",
         "Apply Terraform module aws_backup_plan across production RDS instances.",
         "Destroy terraform backup vault plan if retention lifecycle triggers rate limiting.",
         "Trigger manual snapshot creation and verify restore to test instance.",
         now - timedelta(hours=1), now + timedelta(hours=2), "Elena Rostova (IT Manager)", now - timedelta(hours=4))
    ]
    for cnum, title, ctype, status, req, team, desc, reason, risk, imp, iplan, rplan, tplan, sstart, send, appname, appdate in chg_seeds:
        db.add(Change(
            change_number=cnum,
            title=title,
            change_type=ctype,
            status=status,
            requester_name=req,
            assigned_team=team,
            description=desc,
            reason_for_change=reason,
            risk_level=risk,
            impact_level=imp,
            implementation_plan=iplan,
            rollback_plan=rplan,
            test_plan=tplan,
            scheduled_start=sstart,
            scheduled_end=send,
            actual_start=sstart if status in [ChangeStatus.IMPLEMENTATION, ChangeStatus.COMPLETED] else None,
            actual_end=send if status == ChangeStatus.COMPLETED else None,
            approver_name=appname,
            approval_date=appdate,
            created_at=now - timedelta(days=3)
        ))
    db.flush()

    # 11. Notifications
    notifs = [
        ("CRITICAL ALERT: INC-1025 Created", "Database-01 CPU reached 94.2%. P1 Incident INC-1025 automatically logged.", "Alert", "Critical", False, "/incidents/25"),
        ("Jira Issue ITSM-245 Linked", "Incident INC-1025 successfully linked with Jira issue ITSM-245 for Database SRE on-call team.", "DevOps", "Info", False, "/devops"),
        ("Change CHG-4001 Approved", "Normal Change CHG-4001 approved by Elena Rostova for database query optimization.", "Change", "Success", True, "/changes"),
        ("SLA Warning: INC-1009 Approaching Resolution Due", "P1 Incident INC-1009 has 18 minutes remaining before resolution SLA breach.", "SLA", "Warning", False, "/incidents/9"),
        ("Service Request REQ-2001 Approved", "AWS Sandbox Account request has been approved and credentials provisioned.", "Incident", "Success", True, "/service-requests")
    ]
    for title, msg, ntype, sev, is_read, link in notifs:
        db.add(Notification(
            title=title,
            message=msg,
            notification_type=ntype,
            severity=sev,
            is_read=is_read,
            link=link,
            created_at=now - timedelta(minutes=15)
        ))

    # 12. Audit Logs
    audits = [
        ("admin", "USER_LOGIN", "User", "1", "Administrator logged in from IP 192.168.1.100", "192.168.1.100"),
        ("Telemetry Engine", "AUTOMATED_INCIDENT_CREATED", "Incident", "INC-1025", "Automated P1 incident created for Database-01 metric spike (CPU=94.2%)", "10.0.4.12"),
        ("admin", "JIRA_SYNC", "DevOps", "ITSM-245", "Synchronized incident INC-1025 with Jira issue ITSM-245", "10.0.9.15"),
        ("itmanager", "CHANGE_APPROVED", "Change", "CHG-4001", "Approved change request CHG-4001 for database performance optimization", "192.168.2.14"),
        ("srelead", "INCIDENT_RESOLVED", "Incident", "INC-1002", "Resolved incident INC-1002: Refreshed SAML signing certificate in IdP", "192.168.1.104"),
    ]
    for user_n, act, rtype, rid, det, ip in audits:
        db.add(AuditLog(
            username=user_n,
            action=act,
            resource_type=rtype,
            resource_id=rid,
            details=det,
            ip_address=ip,
            timestamp=now - timedelta(minutes=30)
        ))

    db.commit()
    print("Database successfully seeded with comprehensive ITSM enterprise demo data!")
