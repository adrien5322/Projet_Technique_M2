"""Telemetry routes for heartbeat monitoring."""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db import get_db
from app.auth.dependencies import require_analyst_or_admin, require_admin, verify_agent_or_user, rate_limit_agent
from app.models.user import User
from app.models.telemetry import TelemetryHeartbeat
from app.schemas.telemetry import (
    TelemetryHeartbeatCreate,
    TelemetryHeartbeatResponse,
    TelemetryStatusSummary,
    MissedHeartbeatInfo,
)
from app.telemetry.service import (
    create_heartbeat,
    get_heartbeat_by_asset,
    get_latest_heartbeat,
    check_missed_heartbeats,
    get_overall_status,
)

router = APIRouter(prefix="/api/v1/telemetry", tags=["telemetry"])


@router.post("/heartbeat", response_model=TelemetryHeartbeatResponse, status_code=status.HTTP_201_CREATED)
async def receive_heartbeat(
    heartbeat_data: TelemetryHeartbeatCreate,
    request: Request,
    db: Session = Depends(get_db),
    _rate_limit: bool = Depends(rate_limit_agent),
    auth=Depends(verify_agent_or_user),
) -> TelemetryHeartbeat:
    """
    Receive a heartbeat from an asset.

    Accepts authentication via:
    - JWT Bearer token (analyst or admin role)
    - X-Agent-Secret header (agent authentication)

    - **asset_id**: Asset ID (optional for now)
    - **status**: Asset status (online, offline, warning)
    - **cpu_usage**: CPU usage percentage (0-100)
    - **memory_usage**: Memory usage percentage (0-100)
    - **disk_usage**: Disk usage percentage (0-100)
    - **network_latency**: Network latency in milliseconds
    """
    return create_heartbeat(db, heartbeat_data)


# IMPORTANT: Specific routes MUST be defined BEFORE parameterized routes like /{asset_id}
@router.get("/status", response_model=dict)
async def get_overall_telemetry_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> dict:
    """
    Get overall telemetry status summary.
    
    Returns counts of online, offline, warning assets and missed heartbeats.
    """
    return get_overall_status(db)


@router.get("/missed", response_model=List[dict])
async def get_missed_heartbeats(
    timeout_minutes: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> List[dict]:
    """
    Get list of assets that missed their heartbeat.
    
    - **timeout_minutes**: Number of minutes after which a heartbeat is considered missed (default: 5)
    
    Requires admin role.
    """
    missed_asset_ids = check_missed_heartbeats(db, timeout_minutes)
    
    result = []
    for asset_id in missed_asset_ids:
        latest = get_latest_heartbeat(db, asset_id)
        minutes_since_last = None
        if latest and latest.timestamp:
            minutes_since_last = (datetime.utcnow() - latest.timestamp).total_seconds() / 60
        
        result.append({
            'asset_id': asset_id,
            'last_heartbeat': latest.timestamp if latest else None,
            'minutes_since_last': minutes_since_last,
        })
    
    return result


@router.get("/latest/{asset_id}", response_model=Optional[TelemetryHeartbeatResponse])
async def get_latest_asset_heartbeat(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> Optional[TelemetryHeartbeat]:
    """
    Get the latest heartbeat for a specific asset.
    
    - **asset_id**: Asset ID to query
    """
    return get_latest_heartbeat(db, asset_id)


@router.get("/{asset_id}", response_model=List[TelemetryHeartbeatResponse])
async def get_telemetry_history(
    asset_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> List[TelemetryHeartbeat]:
    """
    Get telemetry history for a specific asset.
    
    - **asset_id**: Asset ID to query
    - **limit**: Maximum number of records to return (default: 100)
    """
    return get_heartbeat_by_asset(db, asset_id, limit)
