"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", status_code=200)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns the application status and version.
    """
    from app.config import settings
    
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
