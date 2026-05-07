"""UI routes for serving HTML dashboard pages."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.auth.dependencies import require_analyst_or_admin
from app.models.user import User

BASE_DIR = Path(__file__).resolve().parent.parent / "ui" / "templates"

templates = Jinja2Templates(directory=str(BASE_DIR))

router = APIRouter(tags=["Dashboard UI"])


@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request, current_user: User = Depends(require_analyst_or_admin)):
    return templates.TemplateResponse(request, "dashboard.html", {"user": current_user})


@router.get("/assets", response_class=HTMLResponse)
async def assets_page(request: Request, current_user: User = Depends(require_analyst_or_admin)):
    return templates.TemplateResponse(request, "assets.html", {"user": current_user})


@router.get("/events", response_class=HTMLResponse)
async def events_page(request: Request, current_user: User = Depends(require_analyst_or_admin)):
    return templates.TemplateResponse(request, "events.html", {"user": current_user})


@router.get("/alerts", response_class=HTMLResponse)
async def alerts_page(request: Request, current_user: User = Depends(require_analyst_or_admin)):
    return templates.TemplateResponse(request, "alerts.html", {"user": current_user})


@router.get("/attackers", response_class=HTMLResponse)
async def attackers_page(request: Request, current_user: User = Depends(require_analyst_or_admin)):
    return templates.TemplateResponse(request, "attackers.html", {"user": current_user})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")
