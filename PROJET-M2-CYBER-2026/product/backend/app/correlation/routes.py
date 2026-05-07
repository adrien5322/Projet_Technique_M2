"""Correlation routes for managing correlation groups."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.db import get_db
from app.auth.dependencies import get_current_user, require_analyst_or_admin, require_admin
from app.models.user import User
from app.models.correlation import CorrelationGroup
from app.schemas.correlation import (
    CorrelationGroupResponse,
    CorrelationGroupListResponse,
    CorrelationGroupUpdate,
    CorrelationStatsResponse,
)

router = APIRouter(prefix="/api/v1/correlations", tags=["Correlation"])


@router.post("/run", response_model=List[CorrelationGroupResponse], status_code=status.HTTP_201_CREATED)
async def run_correlation(
    window_minutes_ip: int = Query(30, ge=5, le=120, description="Time window in minutes for IP correlation"),
    min_events_ip: int = Query(3, ge=2, le=20, description="Minimum events for IP correlation"),
    window_minutes_temp: int = Query(15, ge=5, le=60, description="Time window in minutes for temporal correlation"),
    min_events_temp: int = Query(5, ge=2, le=20, description="Minimum events for temporal correlation"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),  # Only admin can trigger correlation
):
    """Run correlation algorithms to group events.
    
    This endpoint triggers IP-based and temporal correlation.
    Only admin users can trigger correlation.
    """
    from app.correlation.service import run_ip_correlation, run_temporal_correlation
    
    # Run IP correlation
    ip_groups = run_ip_correlation(db, window_minutes=window_minutes_ip, min_events=min_events_ip)
    
    # Run temporal correlation
    temp_groups = run_temporal_correlation(db, window_minutes=window_minutes_temp, min_events=min_events_temp)
    
    # Combine results
    all_groups = ip_groups + temp_groups
    
    return all_groups


@router.get("/", response_model=CorrelationGroupListResponse)
async def list_correlation_groups(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return"),
    status_filter: Optional[str] = Query(None, description="Filter by status (open, investigating, resolved, false_positive)"),
    rule_type_filter: Optional[str] = Query(None, description="Filter by rule type (ip_source, temporal)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    """List correlation groups with filtering and pagination."""
    from app.correlation.service import get_correlation_groups
    
    groups, total = get_correlation_groups(
        db, 
        skip=skip, 
        limit=limit, 
        status_filter=status_filter, 
        rule_type_filter=rule_type_filter
    )
    
    return CorrelationGroupListResponse(
        items=groups,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/stats", response_model=CorrelationStatsResponse)
async def get_correlation_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    """Get correlation statistics (counts by rule type, status, severity)."""
    from app.correlation.service import get_correlation_stats
    
    stats = get_correlation_stats(db)
    
    return CorrelationStatsResponse(**stats)


@router.get("/{group_id}", response_model=CorrelationGroupResponse)
async def get_correlation_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    """Get details of a specific correlation group including its events."""
    from app.correlation.service import get_correlation_group as get_group
    
    group = get_group(db, group_id)
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Correlation group with ID {group_id} not found"
        )
    
    return group


@router.patch("/{group_id}", response_model=CorrelationGroupResponse)
async def update_correlation_group(
    group_id: int,
    update_data: CorrelationGroupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    """Update a correlation group (status and/or assigned_to)."""
    from app.correlation.service import update_correlation_group as update_group
    
    # Convert to dict, excluding unset values
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # If assigning to someone, verify the user exists
    if "assigned_to" in update_dict and update_dict["assigned_to"] is not None:
        from app.models.user import User as UserModel
        assignee = db.query(UserModel).filter(UserModel.id == update_dict["assigned_to"]).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {update_dict['assigned_to']} not found"
            )
    
    group = update_group(db, group_id, update_dict)
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Correlation group with ID {group_id} not found"
        )
    
    return group
