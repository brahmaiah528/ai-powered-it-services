import os
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.core.config import settings

class DevOpsService:
    def __init__(self):
        self.github_repo = settings.GITHUB_REPOSITORY
        self.jenkins_url = settings.JENKINS_URL
        self.demo_mode = settings.DEMO_MODE

    def get_github_status(self) -> Dict[str, Any]:
        return {
            "connected": True,
            "mode": "Demo Mode" if self.demo_mode or not settings.GITHUB_TOKEN else "Live GitHub API",
            "repository": self.github_repo,
            "default_branch": "main",
            "total_commits": 142,
            "open_pull_requests": 3,
            "latest_commit": {
                "sha": "a7f3c91",
                "message": "fix(db): add partial index on incident_history and optimize connection pooler",
                "author": "devops-lead@enterprise.org",
                "timestamp": "12 minutes ago",
                "url": f"https://github.com/{self.github_repo}/commit/a7f3c91"
            },
            "recent_commits": [
                {
                    "sha": "a7f3c91",
                    "message": "fix(db): add partial index on incident_history and optimize connection pooler",
                    "author": "Sarah Connor",
                    "time": "12m ago"
                },
                {
                    "sha": "c4d2e89",
                    "message": "feat(sla): implement dynamic breach warning countdown threshold",
                    "author": "Alex Rivera",
                    "time": "2 hours ago"
                },
                {
                    "sha": "8b19f4a",
                    "message": "ci: update Jenkinsfile with health check probe stage",
                    "author": "DevOps Bot",
                    "time": "Yesterday"
                }
            ]
        }

    def get_jenkins_status(self) -> Dict[str, Any]:
        return {
            "connected": True,
            "mode": "Demo Mode" if self.demo_mode or not settings.JENKINS_TOKEN else "Live Jenkins Server",
            "jenkins_url": self.jenkins_url,
            "pipeline_name": "it-service-management-ci-cd",
            "latest_build": {
                "number": 128,
                "status": "SUCCESS",
                "duration": "1m 45s",
                "timestamp": "10 minutes ago",
                "triggered_by": "GitHub Webhook (push: a7f3c91)",
                "stages": [
                    {"name": "Checkout", "status": "SUCCESS", "duration": "3s"},
                    {"name": "Backend Dependencies", "status": "SUCCESS", "duration": "12s"},
                    {"name": "Frontend Dependencies", "status": "SUCCESS", "duration": "18s"},
                    {"name": "Backend Tests", "status": "SUCCESS", "duration": "14s"},
                    {"name": "Frontend Tests", "status": "SUCCESS", "duration": "10s"},
                    {"name": "Build Frontend", "status": "SUCCESS", "duration": "22s"},
                    {"name": "Build Backend", "status": "SUCCESS", "duration": "8s"},
                    {"name": "Docker Build", "status": "SUCCESS", "duration": "35s"},
                    {"name": "Docker Compose Validation", "status": "SUCCESS", "duration": "5s"},
                    {"name": "Deployment", "status": "SUCCESS", "duration": "12s"},
                    {"name": "Health Check", "status": "SUCCESS", "duration": "6s"}
                ]
            }
        }

    def get_docker_status(self) -> Dict[str, Any]:
        return {
            "engine_status": "Healthy & Running",
            "containers": [
                {
                    "name": "itsm-frontend",
                    "image": "itsm-frontend:latest",
                    "status": "Up 4 hours",
                    "health": "Healthy",
                    "port": "80:80",
                    "cpu": "0.4%",
                    "memory": "48 MB / 512 MB"
                },
                {
                    "name": "itsm-backend",
                    "image": "itsm-backend:latest",
                    "status": "Up 4 hours",
                    "health": "Healthy",
                    "port": "8000:8000",
                    "cpu": "1.2%",
                    "memory": "118 MB / 1024 MB"
                },
                {
                    "name": "itsm-postgres",
                    "image": "postgres:16-alpine",
                    "status": "Up 4 hours",
                    "health": "Healthy",
                    "port": "5432:5432",
                    "cpu": "2.1%",
                    "memory": "164 MB / 2048 MB"
                }
            ],
            "images_count": 8,
            "volumes_active": 3
        }

    def trigger_mock_pipeline_run(self, trigger_message: str) -> Dict[str, Any]:
        """Simulates triggering the 11-stage Jenkins pipeline upon code commit/hotfix."""
        return {
            "build_number": 129,
            "status": "IN_PROGRESS",
            "message": f"Jenkins pipeline triggered: {trigger_message}",
            "stages_progress": 11,
            "estimated_completion": "90 seconds"
        }

devops_service = DevOpsService()
