"""Telemetry service for heartbeat operations."""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from app.models.telemetry import TelemetryHeartbeat
from app.schemas.telemetry import TelemetryHeartbeatCreate


def create_heartbeat(db: Session, heartbeat_data: TelemetryHeartbeatCreate) -> TelemetryHeartbeat:
    """
    Create a new heartbeat record.
    
    Args:
        db: Database session
        heartbeat_data: Heartbeat data to create
        
    Returns:
        Created TelemetryHeartbeat instance
    """
    db_heartbeat = TelemetryHeartbeat(
        asset_id=heartbeat_data.asset_id,
        status=heartbeat_data.status,
        cpu_usage=heartbeat_data.cpu_usage,
        memory_usage=heartbeat_data.memory_usage,
        disk_usage=heartbeat_data.disk_usage,
        network_latency=heartbeat_data.network_latency,
    )
    
    db.add(db_heartbeat)
    db.commit()
    db.refresh(db_heartbeat)
    
    return db_heartbeat


def get_heartbeat_by_asset(db: Session, asset_id: int, limit: int = 100) -> List[TelemetryHeartbeat]:
    """
    Get heartbeat history for a specific asset.
    
    Args:
        db: Database session
        asset_id: Asset ID to query
        limit: Maximum number of records to return (default: 100)
        
    Returns:
        List of TelemetryHeartbeat instances
    """
    return (
        db.query(TelemetryHeartbeat)
        .filter(TelemetryHeartbeat.asset_id == asset_id)
        .order_by(desc(TelemetryHeartbeat.timestamp))
        .limit(limit)
        .all()
    )


def get_latest_heartbeat(db: Session, asset_id: int) -> Optional[TelemetryHeartbeat]:
    """
    Get the latest heartbeat for a specific asset.
    
    Args:
        db: Database session
        asset_id: Asset ID to query
        
    Returns:
        Latest TelemetryHeartbeat instance or None
    """
    return (
        db.query(TelemetryHeartbeat)
        .filter(TelemetryHeartbeat.asset_id == asset_id)
        .order_by(desc(TelemetryHeartbeat.timestamp))
        .first()
    )


def check_missed_heartbeats(db: Session, timeout_minutes: int = 5) -> List[int]:
    """
    Check for assets that have missed their heartbeat.
    
    Args:
        db: Database session
        timeout_minutes: Number of minutes after which a heartbeat is considered missed
        
    Returns:
        List of asset IDs that have missed heartbeats
    """
    cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
    
    # Subquery to get the latest heartbeat for each asset
    latest_heartbeats = (
        db.query(
            TelemetryHeartbeat.asset_id,
            func.max(TelemetryHeartbeat.timestamp).label('last_heartbeat')
        )
        .group_by(TelemetryHeartbeat.asset_id)
        .subquery()
    )
    
    # Find assets whose last heartbeat is older than cutoff time
    missed_assets = (
        db.query(latest_heartbeats.c.asset_id)
        .filter(latest_heartbeats.c.last_heartbeat < cutoff_time)
        .all()
    )
    
    return [asset_id for (asset_id,) in missed_assets]


def get_overall_status(db: Session, timeout_minutes: int = 5) -> dict:
    """
    Get overall telemetry status summary.
    
    Args:
        db: Database session
        timeout_minutes: Number of minutes to consider a heartbeat as recent
        
    Returns:
        Dictionary with status summary
    """
    cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
    
    # Get all assets with their latest heartbeat
    latest_heartbeats = (
        db.query(TelemetryHeartbeat)
        .distinct(TelemetryHeartbeat.asset_id)
        .order_by(TelemetryHeartbeat.asset_id, desc(TelemetryHeartbeat.timestamp))
        .all()
    )
    
    # Count by status (only consider heartbeats within timeout)
    online_count = 0
    offline_count = 0
    warning_count = 0
    
    for heartbeat in latest_heartbeats:
        if heartbeat.timestamp >= cutoff_time:
            if heartbeat.status == 'online':
                online_count += 1
            elif heartbeat.status == 'offline':
                offline_count += 1
            elif heartbeat.status == 'warning':
                warning_count += 1
    
    total_assets = len(set(hb.asset_id for hb in latest_heartbeats if hb.timestamp >= cutoff_time))
    missed_count = len(check_missed_heartbeats(db, timeout_minutes))
    
    return {
        'total_assets': total_assets,
        'online_count': online_count,
        'offline_count': offline_count,
        'warning_count': warning_count,
        'missed_heartbeats_count': missed_count,
    }
