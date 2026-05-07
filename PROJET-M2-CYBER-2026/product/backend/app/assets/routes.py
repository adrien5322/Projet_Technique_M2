"""Asset routes for inventory management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app.auth.dependencies import require_analyst_or_admin, require_admin
from app.models.user import User
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse, AssetListResponse
from app.assets.service import (
    create_asset,
    get_asset,
    get_assets,
    update_asset,
    delete_asset,
    update_last_seen,
)

router = APIRouter(prefix="/api/v1/assets", tags=["Assets"])


@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset_endpoint(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> AssetResponse:
    """
    Create a new asset.
    
    Requires admin role.
    """
    return create_asset(db, asset_data)


@router.get("/", response_model=AssetListResponse)
async def list_assets_endpoint(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> AssetListResponse:
    """
    List all assets with optional filters.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (pagination)
    - **status_filter**: Filter by asset status (active/inactive/maintenance)
    - **type_filter**: Filter by asset type (server/workstation/laptop/mobile/iot)
    
    Requires analyst or admin role.
    """
    assets, total = get_assets(db, skip, limit, status_filter, type_filter)
    return AssetListResponse(
        items=assets,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset_endpoint(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
) -> AssetResponse:
    """
    Get details of a specific asset.
    
    - **asset_id**: Asset ID to retrieve
    
    Requires analyst or admin role.
    """
    asset = get_asset(db, asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found",
        )
    return asset


@router.put("/{asset_id}", response_model=AssetResponse)
async def update_asset_endpoint(
    asset_id: int,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> AssetResponse:
    """
    Update an existing asset.
    
    - **asset_id**: Asset ID to update
    - **asset_data**: Updated asset data (partial updates supported)
    
    Requires admin role.
    """
    updated_asset = update_asset(db, asset_id, asset_data)
    if not updated_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found",
        )
    return updated_asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset_endpoint(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> None:
    """
    Delete an asset.
    
    - **asset_id**: Asset ID to delete
    
    Requires admin role.
    """
    if not delete_asset(db, asset_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found",
        )
