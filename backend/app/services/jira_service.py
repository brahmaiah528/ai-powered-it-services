import json
import base64
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import httpx
from app.core.config import settings

class JiraService:
    def __init__(self):
        self.url = settings.JIRA_URL.rstrip('/')
        self.email = settings.JIRA_EMAIL
        self.api_token = settings.JIRA_API_TOKEN
        self.project_key = settings.JIRA_PROJECT_KEY
        self.is_live = bool(self.api_token and self.api_token != "your_jira_api_token_here" and not settings.DEMO_MODE)
        
        # In-memory mock storage for demo mode
        self.mock_issues = {
            "ITSM-245": {
                "key": "ITSM-245",
                "summary": "Critical: Database Server CPU exceeded 90% (Linked: INC-1025)",
                "description": "Database-01 experiencing high load. Automated P1 incident created. Needs hotfix query index optimization.",
                "status": "In Progress",
                "priority": "Highest",
                "assignee": "Sarah Connor (Database SRE)",
                "project": "ITSM",
                "created": "2026-09-02T08:30:00Z",
                "url": f"{self.url}/browse/ITSM-245"
            },
            "ITSM-246": {
                "key": "ITSM-246",
                "summary": "Fix SSO Token Expiry Issue on Internal Gateway (Linked: INC-1002)",
                "description": "Users intermittently receiving HTTP 401 on legacy portal due to token clock skew.",
                "status": "Done",
                "priority": "High",
                "assignee": "Alex Rivera (Platform Eng)",
                "project": "ITSM",
                "created": "2026-09-01T14:10:00Z",
                "url": f"{self.url}/browse/ITSM-246"
            }
        }
        self.next_issue_id = 247

    def _get_auth_headers(self) -> Dict[str, str]:
        auth_str = f"{self.email}:{self.api_token}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        return {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def create_issue(
        self,
        incident_number: str,
        summary: str,
        description: str,
        priority: str = "High",
        issue_type: str = "Bug"
    ) -> Dict[str, Any]:
        """Create a Jira issue linked to an ITSM incident."""
        if self.is_live:
            try:
                payload = {
                    "fields": {
                        "project": {"key": self.project_key},
                        "summary": f"[{incident_number}] {summary}",
                        "description": f"ITSM Incident: {incident_number}\n\n{description}\n\nAutomated via AI ITSM Platform.",
                        "issuetype": {"name": issue_type},
                        "priority": {"name": "High" if "P1" in priority or "P2" in priority else "Medium"}
                    }
                }
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        f"{self.url}/rest/api/2/issue",
                        headers=self._get_auth_headers(),
                        json=payload
                    )
                    if resp.status_code in [200, 201]:
                        data = resp.json()
                        key = data.get("key", f"{self.project_key}-{self.next_issue_id}")
                        return {
                            "jira_key": key,
                            "url": f"{self.url}/browse/{key}",
                            "status": "To Do",
                            "priority": priority,
                            "sync_status": "Linked & Synchronized",
                            "is_mock": False
                        }
            except Exception as e:
                # Fallback to simulation mode gracefully if live connection fails
                pass

        # Demo / Simulation Mode
        key = f"{self.project_key}-{self.next_issue_id}"
        self.next_issue_id += 1
        issue_data = {
            "key": key,
            "summary": f"[{incident_number}] {summary}",
            "description": description,
            "status": "To Do",
            "priority": priority,
            "assignee": "Enterprise SRE On-Call Team",
            "project": self.project_key,
            "created": datetime.now(timezone.utc).isoformat(),
            "url": f"{self.url}/browse/{key}"
        }
        self.mock_issues[key] = issue_data
        return {
            "jira_key": key,
            "url": issue_data["url"],
            "status": "To Do",
            "priority": priority,
            "sync_status": "Linked & Synchronized (Demo Mode)",
            "is_mock": True
        }

    async def sync_issue(self, jira_key: str) -> Dict[str, Any]:
        """Synchronize Jira issue status, priority, and updates."""
        if self.is_live:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(
                        f"{self.url}/rest/api/2/issue/{jira_key}",
                        headers=self._get_auth_headers()
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        fields = data.get("fields", {})
                        return {
                            "jira_key": jira_key,
                            "status": fields.get("status", {}).get("name", "In Progress"),
                            "priority": fields.get("priority", {}).get("name", "High"),
                            "assignee": fields.get("assignee", {}).get("displayName", "Assigned SRE"),
                            "url": f"{self.url}/browse/{jira_key}",
                            "sync_status": "In Sync",
                            "last_synced": datetime.now(timezone.utc).isoformat(),
                            "is_mock": False
                        }
            except Exception:
                pass
                
        # Demo Mode Sync
        issue = self.mock_issues.get(jira_key, {
            "key": jira_key,
            "status": "In Progress",
            "priority": "High",
            "assignee": "Enterprise SRE Lead",
            "url": f"{self.url}/browse/{jira_key}"
        })
        return {
            "jira_key": jira_key,
            "status": issue.get("status", "In Progress"),
            "priority": issue.get("priority", "High"),
            "assignee": issue.get("assignee", "DevOps Engineer"),
            "url": issue.get("url", f"{self.url}/browse/{jira_key}"),
            "sync_status": "In Sync (Demo Mode)",
            "last_synced": datetime.now(timezone.utc).isoformat(),
            "is_mock": True
        }

jira_service = JiraService()
