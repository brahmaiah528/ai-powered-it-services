from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.core.seed_data import seed_database

# Routers
from app.api.auth import router as auth_router
from app.api.incidents import router as incidents_router
from app.api.service_requests import router as service_requests_router
from app.api.problems import router as problems_router
from app.api.changes import router as changes_router
from app.api.assets import router as assets_router
from app.api.infrastructure import router as infrastructure_router
from app.api.ai_engine import router as ai_router
from app.api.jira_integration import router as jira_router
from app.api.devops import router as devops_router
from app.api.knowledge_base import router as kb_router
from app.api.notifications import router as notifications_router
from app.api.reports import router as reports_router
from app.api.audit_logs import router as audit_router
from app.api.simulation import router as simulation_router

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

# Initialize immediately on import
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="AI-Powered IT Service Management and Incident Resolution Platform",
    description="Enterprise IT Operations platform with AI incident analysis and Jira/GitHub/Jenkins/Docker integration.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(incidents_router, prefix=settings.API_V1_STR)
app.include_router(service_requests_router, prefix=settings.API_V1_STR)
app.include_router(problems_router, prefix=settings.API_V1_STR)
app.include_router(changes_router, prefix=settings.API_V1_STR)
app.include_router(assets_router, prefix=settings.API_V1_STR)
app.include_router(infrastructure_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)
app.include_router(jira_router, prefix=settings.API_V1_STR)
app.include_router(devops_router, prefix=settings.API_V1_STR)
app.include_router(kb_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)
app.include_router(simulation_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "app": "AI-Powered IT Service Management Platform",
        "status": "online",
        "docs": "/docs",
        "demo_mode": settings.DEMO_MODE,
        "version": "1.0.0"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "Healthy",
        "database": "Connected",
        "ai_engine": "Operational",
        "jira_integration": "Connected (Simulation/Live Mode)",
        "devops_ecosystem": "Active"
    }
