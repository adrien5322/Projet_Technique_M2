"""Discovery routes for network scanning and port discovery."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth.dependencies import require_analyst_or_admin, require_admin
from app.models.user import User
from app.config import settings
from app.schemas.discovery import IPRangeScanRequest
from app.schemas.port_finding import (
    PortFindingResponse,
    PortFindingListResponse,
)
from app.schemas.asset import AssetResponse
from app.discovery.service import (
    scan_ip_range,
    scan_ports,
    get_port_findings_by_asset,
)

router = APIRouter(prefix="/api/v1/discovery", tags=["Discovery"])


@router.post("/scan", status_code=status.HTTP_200_OK)
async def trigger_ip_scan(
    request: IPRangeScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict:
    """
    Trigger a network scan on an IP range.

    - **ip_range**: CIDR notation (e.g. "192.168.1.0/24")

    Requires admin role.
    """
    try:
        assets = scan_ip_range(request.ip_range, db, timeout=settings.NMAP_TIMEOUT)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "message": f"Scan completed for range {request.ip_range}",
        "assets_found": len(assets),
        "assets": [
            {"id": a.id, "hostname": a.hostname, "ip_address": a.ip_address}
            for a in assets
        ],
    }


@router.post("/ports/{asset_id}", response_model=list[PortFindingResponse], status_code=status.HTTP_200_OK)
async def trigger_port_scan(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[PortFindingResponse]:
    """
    Trigger a port scan on a specific asset.

    - **asset_id**: ID of the asset to scan

    Requires admin role.
    """
    try:
        findings = scan_ports(asset_id, db, timeout=settings.NMAP_TIMEOUT)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return findings


@router.get("/ports/{asset_id}", response_model=PortFindingListResponse)
async def list_port_findings(
    asset_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> PortFindingListResponse:
    """
    List port findings for a specific asset.

    - **asset_id**: ID of the asset
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return

    Requires analyst or admin role.
    """
    findings, total = get_port_findings_by_asset(db, asset_id, skip, limit)
    return PortFindingListResponse(
        items=findings,
        total=total,
        skip=skip,
        limit=limit,
    )
