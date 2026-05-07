"""Asset service for inventory management operations."""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


def create_asset(db: Session, asset_data: AssetCreate) -> Asset:
    """
    Create a new asset.
    
    Args:
        db: Database session
        asset_data: Asset creation data
        
    Returns:
        Created Asset instance
    """
    # Convert Pydantic model to dict, excluding unset values
    asset_dict = asset_data.model_dump()
    
    # Create Asset instance
    db_asset = Asset(**asset_dict)
    
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    
    return db_asset


def get_asset(db: Session, asset_id: int) -> Optional[Asset]:
    """
    Get a specific asset by ID.
    
    Args:
        db: Database session
        asset_id: Asset ID to retrieve
        
    Returns:
        Asset instance or None if not found
    """
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_assets(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
) -> tuple[List[Asset], int]:
    """
    Get list of assets with optional filtering and pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        status_filter: Filter by asset status
        type_filter: Filter by asset type
        
    Returns:
        Tuple of (list of Asset instances, total count)
    """
    query = db.query(Asset)
    
    # Apply filters
    if status_filter:
        query = query.filter(Asset.status == status_filter)
    if type_filter:
        query = query.filter(Asset.asset_type == type_filter)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination and ordering
    assets = query.order_by(desc(Asset.created_at)).offset(skip).limit(limit).all()
    
    return assets, total


def update_asset(db: Session, asset_id: int, asset_data: AssetUpdate) -> Optional[Asset]:
    """
    Update an existing asset.
    
    Args:
        db: Database session
        asset_id: Asset ID to update
        asset_data: Asset update data (only provided fields are updated)
        
    Returns:
        Updated Asset instance or None if not found
    """
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    
    # Update only provided fields
    update_data = asset_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.commit()
    db.refresh(db_asset)
    
    return db_asset


def delete_asset(db: Session, asset_id: int) -> bool:
    """
    Delete an asset.
    
    Args:
        db: Database session
        asset_id: Asset ID to delete
        
    Returns:
        True if deleted, False if not found
    """
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return False
    
    db.delete(db_asset)
    db.commit()
    
    return True


def update_last_seen(db: Session, asset_id: int) -> Optional[Asset]:
    """
    Update the last_seen timestamp for an asset.
    Called when a heartbeat is received.
    
    Args:
        db: Database session
        asset_id: Asset ID to update
        
    Returns:
        Updated Asset instance or None if not found
    """
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    
    db_asset.last_seen = datetime.utcnow()
    db.commit()
    db.refresh(db_asset)
    
    return db_asset
