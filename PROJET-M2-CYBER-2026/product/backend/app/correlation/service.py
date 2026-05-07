"""Correlation service for event correlation logic."""

from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.correlation import CorrelationGroup, correlation_events
from app.models.event import Event
from app.schemas.correlation import CorrelationGroupCreate


def calculate_severity_bonus(severity: str) -> int:
    """Calculate bonus score based on event severity."""
    severity_bonus_map = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5,
    }
    return severity_bonus_map.get(severity.lower(), 0)


def calculate_correlation_score(event_count: int, severities: List[str]) -> int:
    """Calculate correlation score based on event count and severities.
    
    Score = min(100, event_count * 10 + sum of severity bonuses)
    """
    base_score = event_count * 10
    severity_bonus = sum(calculate_severity_bonus(s) for s in severities)
    return min(100, base_score + severity_bonus)


def get_severity_from_score(events: List[Event]) -> str:
    """Determine the highest severity from a list of events."""
    severity_priority = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    severities = [e.severity for e in events if e.severity]
    if not severities:
        return "medium"
    return max(severities, key=lambda s: severity_priority.get(s.lower(), 0))


def run_ip_correlation(
    db: Session, 
    window_minutes: int = 30, 
    min_events: int = 3
) -> List[CorrelationGroup]:
    """Run IP-based correlation to group events by source IP.
    
    Finds source IPs with >= min_events in the last window_minutes,
    creates or updates CorrelationGroup for each IP,
    associates events with the group,
    and calculates correlation score.
    """
    # Calculate the time window
    window_start = datetime.utcnow() - timedelta(minutes=window_minutes)
    
    # Find source IPs with enough events in the time window
    ip_query = (
        db.query(
            Event.source_ip,
            func.count(Event.id).label("event_count")
        )
        .filter(
            and_(
                Event.source_ip.isnot(None),
                Event.timestamp >= window_start
            )
        )
        .group_by(Event.source_ip)
        .having(func.count(Event.id) >= min_events)
        .all()
    )
    
    created_groups = []
    
    for source_ip, event_count in ip_query:
        # Get all events for this IP in the time window
        events = (
            db.query(Event)
            .filter(
                and_(
                    Event.source_ip == source_ip,
                    Event.timestamp >= window_start
                )
            )
            .order_by(Event.timestamp.asc())
            .all()
        )
        
        if not events:
            continue
        
        # Check if a correlation group already exists for this IP
        existing_group = (
            db.query(CorrelationGroup)
            .filter(
                and_(
                    CorrelationGroup.rule_type == "ip_source",
                    CorrelationGroup.rule_key == source_ip,
                    CorrelationGroup.status.in_(["open", "investigating"])
                )
            )
            .first()
        )
        
        # Calculate values
        severities = [e.severity for e in events if e.severity]
        score = calculate_correlation_score(len(events), severities)
        severity = get_severity_from_score(events)
        first_seen = min(e.timestamp for e in events)
        last_seen = max(e.timestamp for e in events)
        
        if existing_group:
            # Update existing group
            existing_group.event_count = len(events)
            existing_group.score = score
            existing_group.severity = severity
            existing_group.last_seen = last_seen
            
            # Associate new events
            existing_events_ids = {e.id for e in existing_group.events}
            for event in events:
                if event.id not in existing_events_ids:
                    existing_group.events.append(event)
            
            db.add(existing_group)
            created_groups.append(existing_group)
        else:
            # Create new group
            new_group = CorrelationGroup(
                rule_type="ip_source",
                rule_key=source_ip,
                severity=severity,
                score=score,
                event_count=len(events),
                first_seen=first_seen,
                last_seen=last_seen,
                status="open",
                description=f"IP correlation group for source IP: {source_ip}"
            )
            
            db.add(new_group)
            db.flush()  # Get the ID
            
            # Associate all events
            for event in events:
                new_group.events.append(event)
            
            created_groups.append(new_group)
    
    db.commit()
    
    # Refresh to load relationships
    for group in created_groups:
        db.refresh(group)
    
    return created_groups


def run_temporal_correlation(
    db: Session, 
    window_minutes: int = 15, 
    min_events: int = 5
) -> List[CorrelationGroup]:
    """Run temporal correlation to group events in time clusters.
    
    Finds clusters of events from the same source IP within a short time window,
    creates groups of type "temporal",
    score based on temporal density.
    """
    # Calculate the time window
    window_start = datetime.utcnow() - timedelta(minutes=window_minutes * 2)  # Look back further
    
    # Get events grouped by source IP with timestamps
    events_by_ip = {}
    events = (
        db.query(Event)
        .filter(
            and_(
                Event.source_ip.isnot(None),
                Event.timestamp >= window_start
            )
        )
        .order_by(Event.source_ip, Event.timestamp.asc())
        .all()
    )
    
    # Group events by source IP
    for event in events:
        if event.source_ip not in events_by_ip:
            events_by_ip[event.source_ip] = []
        events_by_ip[event.source_ip].append(event)
    
    created_groups = []
    
    for source_ip, ip_events in events_by_ip.items():
        if len(ip_events) < min_events:
            continue
        
        # Find temporal clusters within this IP's events
        clusters = []
        current_cluster = [ip_events[0]]
        
        for i in range(1, len(ip_events)):
            time_diff = (ip_events[i].timestamp - ip_events[i-1].timestamp).total_seconds() / 60
            if time_diff <= window_minutes:
                current_cluster.append(ip_events[i])
            else:
                if len(current_cluster) >= min_events:
                    clusters.append(current_cluster)
                current_cluster = [ip_events[i]]
        
        # Don't forget the last cluster
        if len(current_cluster) >= min_events:
            clusters.append(current_cluster)
        
        # Create correlation groups for each cluster
        for cluster in clusters:
            cluster_start = min(e.timestamp for e in cluster)
            cluster_end = max(e.timestamp for e in cluster)
            
            # Check if a temporal group already exists for this time range and IP
            existing_group = (
                db.query(CorrelationGroup)
                .filter(
                    and_(
                        CorrelationGroup.rule_type == "temporal",
                        CorrelationGroup.rule_key == f"{source_ip}_{cluster_start.isoformat()}",
                        CorrelationGroup.status.in_(["open", "investigating"])
                    )
                )
                .first()
            )
            
            if existing_group:
                continue  # Skip if already exists
            
            # Calculate values
            severities = [e.severity for e in cluster if e.severity]
            score = calculate_correlation_score(len(cluster), severities)
            severity = get_severity_from_score(cluster)
            
            # Create new temporal group
            new_group = CorrelationGroup(
                rule_type="temporal",
                rule_key=f"{source_ip}_{cluster_start.isoformat()}",
                severity=severity,
                score=score,
                event_count=len(cluster),
                first_seen=cluster_start,
                last_seen=cluster_end,
                status="open",
                description=f"Temporal correlation group for source IP: {source_ip}"
            )
            
            db.add(new_group)
            db.flush()
            
            # Associate events
            for event in cluster:
                new_group.events.append(event)
            
            created_groups.append(new_group)
    
    db.commit()
    
    # Refresh to load relationships
    for group in created_groups:
        db.refresh(group)
    
    return created_groups


def get_correlation_groups(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    rule_type_filter: Optional[str] = None
) -> Tuple[List[CorrelationGroup], int]:
    """Get correlation groups with filtering and pagination."""
    query = db.query(CorrelationGroup)
    
    if status_filter:
        query = query.filter(CorrelationGroup.status == status_filter)
    
    if rule_type_filter:
        query = query.filter(CorrelationGroup.rule_type == rule_type_filter)
    
    total = query.count()
    
    groups = (
        query
        .order_by(CorrelationGroup.last_seen.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return groups, total


def get_correlation_group(db: Session, group_id: int) -> Optional[CorrelationGroup]:
    """Get a specific correlation group by ID."""
    return db.query(CorrelationGroup).filter(CorrelationGroup.id == group_id).first()


def update_correlation_group(
    db: Session, 
    group_id: int, 
    update_data: dict
) -> Optional[CorrelationGroup]:
    """Update a correlation group with provided data."""
    group = db.query(CorrelationGroup).filter(CorrelationGroup.id == group_id).first()
    
    if not group:
        return None
    
    # Update only provided fields
    if "status" in update_data and update_data["status"] is not None:
        group.status = update_data["status"]
    
    if "assigned_to" in update_data:
        group.assigned_to = update_data["assigned_to"]
    
    db.add(group)
    db.commit()
    db.refresh(group)
    
    return group


def get_correlation_stats(db: Session) -> dict:
    """Get correlation statistics."""
    # Total groups
    total_groups = db.query(CorrelationGroup).count()
    
    # By rule type
    by_rule_type = {}
    rule_type_counts = (
        db.query(CorrelationGroup.rule_type, func.count(CorrelationGroup.id))
        .group_by(CorrelationGroup.rule_type)
        .all()
    )
    by_rule_type = {rt: count for rt, count in rule_type_counts}
    
    # By status
    by_status = {}
    status_counts = (
        db.query(CorrelationGroup.status, func.count(CorrelationGroup.id))
        .group_by(CorrelationGroup.status)
        .all()
    )
    by_status = {status: count for status, count in status_counts}
    
    # By severity
    by_severity = {}
    severity_counts = (
        db.query(CorrelationGroup.severity, func.count(CorrelationGroup.id))
        .group_by(CorrelationGroup.severity)
        .all()
    )
    by_severity = {sev: count for sev, count in severity_counts}
    
    # Specific status counts
    open_groups = by_status.get("open", 0)
    investigating_groups = by_status.get("investigating", 0)
    resolved_groups = by_status.get("resolved", 0)
    false_positive_groups = by_status.get("false_positive", 0)
    
    return {
        "total_groups": total_groups,
        "by_rule_type": by_rule_type,
        "by_status": by_status,
        "by_severity": by_severity,
        "open_groups": open_groups,
        "investigating_groups": investigating_groups,
        "resolved_groups": resolved_groups,
        "false_positive_groups": false_positive_groups,
    }
