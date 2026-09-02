import os
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered IT Service Management & Incident Resolution Platform"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "enterprise-itsm-super-secret-jwt-key-production-ready")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    DEMO_MODE: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./itsm.db")
    
    # Jira Integration
    JIRA_URL: str = os.getenv("JIRA_URL", "https://company-itsm.atlassian.net")
    JIRA_EMAIL: str = os.getenv("JIRA_EMAIL", "devops-lead@enterprise.org")
    JIRA_API_TOKEN: str = os.getenv("JIRA_API_TOKEN", "")
    JIRA_PROJECT_KEY: str = os.getenv("JIRA_PROJECT_KEY", "ITSM")
    
    # GitHub Integration
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_REPOSITORY: str = os.getenv("GITHUB_REPOSITORY", "enterprise-org/it-service-management")
    
    # Jenkins Integration
    JENKINS_URL: str = os.getenv("JENKINS_URL", "http://jenkins.internal.company.com:8080")
    JENKINS_USERNAME: str = os.getenv("JENKINS_USERNAME", "jenkins-admin")
    JENKINS_TOKEN: str = os.getenv("JENKINS_TOKEN", "")
    
    # AI Engine
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()
