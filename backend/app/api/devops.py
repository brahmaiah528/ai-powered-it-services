from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.devops_service import devops_service
from app.services.jira_service import jira_service
from app.models.models import AuditLog, Notification

router = APIRouter(prefix="/devops", tags=["DevOps Hub"])

@router.get("/status")
def get_devops_status():
    gh = devops_service.get_github_status()
    jk = devops_service.get_jenkins_status()
    dk = devops_service.get_docker_status()
    jr = {
        "connected": True,
        "mode": "Demo Mode" if not jira_service.is_live else "Live Jira Cloud",
        "url": jira_service.url,
        "project": jira_service.project_key,
        "open_issues_count": len(jira_service.mock_issues),
        "recent_issues": list(jira_service.mock_issues.values())
    }
    
    return {
        "mode": "Demo / Simulation Mode" if gh["mode"] == "Demo Mode" else "Live Connected Ecosystem",
        "github": gh,
        "jira": jr,
        "jenkins": jk,
        "docker": dk
    }

@router.post("/trigger-build")
def trigger_jenkins_build(payload: Dict[str, Any] = None, db: Session = Depends(get_db)):
    msg = payload.get("message", "Manual Jenkins build triggered from ITSM DevOps console") if payload else "Manual Trigger"
    res = devops_service.trigger_mock_pipeline_run(msg)
    
    db.add(Notification(
        title=f"Jenkins Build #{res['build_number']} Started",
        message=f"Pipeline triggered: {msg}",
        notification_type="DevOps",
        severity="Info",
        link="/devops"
    ))
    
    db.add(AuditLog(
        username="DevOps Console",
        action="JENKINS_BUILD_TRIGGERED",
        resource_type="DevOps",
        resource_id=f"BUILD-{res['build_number']}",
        details=f"Triggered Jenkins pipeline #{res['build_number']}: {msg}"
    ))
    db.commit()
    return res

@router.post("/commit-fix")
def simulate_github_commit_and_deploy(payload: Dict[str, Any] = None, db: Session = Depends(get_db)):
    commit_msg = payload.get("message", "fix(db): add partial index and connection pool tuning for Database-01") if payload else "fix: patch issue"
    sha = "e9a1b42"
    
    # 1. Update GitHub status mock
    devops_service.get_github_status()["latest_commit"] = {
        "sha": sha,
        "message": commit_msg,
        "author": "Sarah Connor (Senior SRE)",
        "timestamp": "Just now",
        "url": f"https://github.com/{devops_service.github_repo}/commit/{sha}"
    }

    # 2. Trigger Jenkins Pipeline
    pipe_res = devops_service.trigger_mock_pipeline_run(f"GitHub push: {sha} ({commit_msg})")

    db.add(AuditLog(
        username="Sarah Connor",
        action="GITHUB_COMMIT_PUSH",
        resource_type="DevOps",
        resource_id=sha,
        details=f"Pushed commit {sha} to repository: {commit_msg}"
    ))
    db.commit()

    return {
        "commit": {
            "sha": sha,
            "message": commit_msg,
            "branch": "main",
            "pushed": True
        },
        "jenkins_pipeline": pipe_res
    }
