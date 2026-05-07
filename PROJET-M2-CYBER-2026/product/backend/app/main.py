"""DAR-Cyber Backend - Main Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.config import settings
from app.db import engine

# Création de l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="DAR-Cyber - Security Operations Center Platform",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring"""
    # Check database connectivity
    db_status = "healthy"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": db_status,
    }


# Inclusion des routeurs
# UI Router must be included BEFORE API routers so that "/" matches the dashboard
from app.dashboard.ui import router as ui_router
app.include_router(ui_router, prefix="/dashboard")

from app.dashboard import dashboard_router as dashboard_api_router
app.include_router(dashboard_api_router)

from app.auth.routes import router as auth_router
from app.telemetry.routes import router as telemetry_router
from app.events.routes import router as events_router

app.include_router(auth_router)  # prefix already defined in routes.py
app.include_router(telemetry_router)  # prefix already defined in routes.py
app.include_router(events_router)  # prefix already defined in routes.py

# TODO: Include other routers when modules are implemented
from app.alerts.routes import router as alerts_router
from app.assets.routes import router as assets_router
from app.audit.routes import router as audit_router
from app.correlation.routes import router as correlation_router
from app.discovery.routes import router as discovery_router
from app.reports.routes import router as reports_router

app.include_router(alerts_router)  # prefix already defined in routes.py
app.include_router(assets_router)  # prefix already defined in routes.py
app.include_router(audit_router)  # prefix already defined in routes.py
app.include_router(correlation_router)  # prefix already defined in routes.py
app.include_router(discovery_router)  # prefix already defined in routes.py
# app.include_router(reports_router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(reports_router)  # prefix already defined in routes.py


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
