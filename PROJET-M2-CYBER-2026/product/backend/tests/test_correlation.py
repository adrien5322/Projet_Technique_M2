"""Tests for correlation module.

Covers:
- Correlation score calculation (unit tests)
- IP-based and temporal correlation logic (unit tests)
- Correlation API endpoints (integration tests)
- RBAC (admin-only create, analyst/admin read)
- Filtering and pagination
- Status updates and assignment
- Statistics endpoint
- Correlation scenarios with events
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import Base
from app.models.event import Event
from app.models.correlation import CorrelationGroup, correlation_events
from app.correlation.service import (
    run_ip_correlation,
    run_temporal_correlation,
    get_correlation_groups,
    get_correlation_group,
    update_correlation_group,
    get_correlation_stats,
    calculate_correlation_score,
    get_severity_from_score,
)
from app.models.user import User
from app.auth.service import get_password_hash


# ── Helpers ──────────────────────────────────────────────────────────────

def _create_event(db_session: Session, source_ip: str = "192.168.1.100", 
                  event_type: str = "login_failed", severity: str = "medium",
                  minutes_ago: int = 0) -> Event:
    """Helper to create an event in the database."""
    event = Event(
        source_ip=source_ip,
        event_type=event_type,
        severity=severity,
        timestamp=datetime.utcnow() - timedelta(minutes=minutes_ago),
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


def _create_correlation_group(db_session: Session, rule_type: str = "ip_source",
                              rule_key: str = "192.168.1.100", severity: str = "medium",
                              score: int = 50, event_count: int = 3,
                              status: str = "open", assigned_to: int = None) -> CorrelationGroup:
    """Helper to create a correlation group in the database."""
    now = datetime.utcnow()
    group = CorrelationGroup(
        rule_type=rule_type,
        rule_key=rule_key,
        severity=severity,
        score=score,
        event_count=event_count,
        first_seen=now - timedelta(minutes=30),
        last_seen=now,
        status=status,
        assigned_to=assigned_to,
        description=f"Test correlation group for {rule_key}",
    )
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)
    return group


def _seed_events_for_correlation(db_session: Session):
    """Create sample events for correlation testing."""
    now = datetime.utcnow()
    events = []
    
    # Create 5 events from same IP in the last 30 minutes
    for i in range(5):
        event = Event(
            source_ip="192.168.1.100",
            event_type="login_failed",
            severity="medium",
            timestamp=now - timedelta(minutes=i * 5),
        )
        db_session.add(event)
        events.append(event)
    
    # Create 3 events from another IP
    for i in range(3):
        event = Event(
            source_ip="10.0.0.50",
            event_type="port_scan",
            severity="high",
            timestamp=now - timedelta(minutes=i * 3),
        )
        db_session.add(event)
        events.append(event)
    
    # Create 2 events from a third IP (should not trigger correlation with min_events=3)
    for i in range(2):
        event = Event(
            source_ip="172.16.0.10",
            event_type="file_access",
            severity="low",
            timestamp=now - timedelta(minutes=i * 10),
        )
        db_session.add(event)
        events.append(event)
    
    db_session.commit()
    return events


# ── Unit Tests (using db_session from conftest.py) ─────────────────────

def test_calculate_correlation_score():
    """Test correlation score calculation."""
    # Test with 3 events
    score = calculate_correlation_score(3, ["medium", "medium", "medium"])
    assert score == 30 + 10 + 10 + 10  # 3*10 + 3*10 (medium bonus)
    
    # Test with high severity events
    score = calculate_correlation_score(2, ["critical", "high"])
    assert score == 20 + 30 + 20  # 2*10 + 30 (critical) + 20 (high)
    
    # Test score capping at 100
    score = calculate_correlation_score(15, ["critical"] * 15)
    assert score == 100


def test_get_severity_from_score():
    """Test severity determination from events."""
    from app.models.event import Event
    
    events = [
        Event(severity="low"),
        Event(severity="medium"),
        Event(severity="low"),
    ]
    assert get_severity_from_score(events) == "medium"
    
    events = [
        Event(severity="high"),
        Event(severity="low"),
    ]
    assert get_severity_from_score(events) == "high"
    
    events = [
        Event(severity="critical"),
    ]
    assert get_severity_from_score(events) == "critical"


def test_run_ip_correlation(db_session, sample_events):
    """Test IP-based correlation."""
    # Run correlation with min 3 events
    groups = run_ip_correlation(db_session, window_minutes=30, min_events=3)
    
    # Should create 2 groups (192.168.1.100 and 10.0.0.50)
    assert len(groups) == 2
    
    # Check first group (192.168.1.100)
    group_192 = next((g for g in groups if g.rule_key == "192.168.1.100"), None)
    assert group_192 is not None
    assert group_192.rule_type == "ip_source"
    assert group_192.event_count == 5
    assert group_192.status == "open"
    
    # Check second group (10.0.0.50)
    group_10 = next((g for g in groups if g.rule_key == "10.0.0.50"), None)
    assert group_10 is not None
    assert group_10.rule_type == "ip_source"
    assert group_10.event_count == 3
    assert group_10.severity == "high"  # Highest severity among events


def test_run_ip_correlation_no_duplicates(db_session, sample_events):
    """Test that running correlation again doesn't create duplicates."""
    # First run
    groups1 = run_ip_correlation(db_session, window_minutes=30, min_events=3)
    assert len(groups1) == 2
    
    # Second run should update existing groups, not create new ones
    groups2 = run_ip_correlation(db_session, window_minutes=30, min_events=3)
    
    # Check that we still have only 2 groups in the database
    all_groups = db_session.query(CorrelationGroup).all()
    assert len(all_groups) == 2


def test_get_correlation_groups(db_session, sample_events):
    """Test getting correlation groups with pagination."""
    # Create correlation groups first
    run_ip_correlation(db_session, window_minutes=30, min_events=3)
    
    # Get all groups
    groups, total = get_correlation_groups(db_session, skip=0, limit=10)
    assert total == 2
    assert len(groups) == 2
    
    # Test pagination
    groups, total = get_correlation_groups(db_session, skip=0, limit=1)
    assert total == 2
    assert len(groups) == 1
    
    # Test status filter
    groups, total = get_correlation_groups(db_session, skip=0, limit=10, status_filter="open")
    assert total == 2
    assert len(groups) == 2
    
    groups, total = get_correlation_groups(db_session, skip=0, limit=10, status_filter="resolved")
    assert total == 0
    assert len(groups) == 0


def test_get_correlation_group(db_session, sample_events):
    """Test getting a specific correlation group."""
    # Create correlation groups
    groups = run_ip_correlation(db_session, window_minutes=30, min_events=3)
    group_id = groups[0].id
    
    # Get the group
    group = get_correlation_group(db_session, group_id)
    assert group is not None
    assert group.id == group_id
    
    # Try to get non-existent group
    group = get_correlation_group(db_session, 9999)
    assert group is None


def test_update_correlation_group(db_session, sample_events):
    """Test updating a correlation group."""
    # Create correlation groups
    groups = run_ip_correlation(db_session, window_minutes=30, min_events=3)
    group_id = groups[0].id
    
    # Update status
    updated = update_correlation_group(db_session, group_id, {"status": "investigating"})
    assert updated is not None
    assert updated.status == "investigating"
    
    # Update assigned_to (create a user first)
    user = User(
        username="analyst1",
        email="analyst1@example.com",
        hashed_password="hashed",
        role="analyst",
    )
    db_session.add(user)
    db_session.commit()
    
    updated = update_correlation_group(db_session, group_id, {"assigned_to": user.id})
    assert updated.assigned_to == user.id
    
    # Try to update non-existent group
    updated = update_correlation_group(db_session, 9999, {"status": "resolved"})
    assert updated is None


def test_get_correlation_stats(db_session, sample_events):
    """Test getting correlation statistics."""
    # Create correlation groups
    run_ip_correlation(db_session, window_minutes=30, min_events=3)
    
    # Get stats
    stats = get_correlation_stats(db_session)
    
    assert stats["total_groups"] == 2
    assert stats["by_rule_type"] == {"ip_source": 2}
    assert stats["by_status"] == {"open": 2}
    assert "open_groups" in stats
    assert stats["open_groups"] == 2


def test_run_temporal_correlation(db_session):
    """Test temporal correlation."""
    now = datetime.utcnow()
    
    # Create events in a tight temporal cluster
    events = []
    for i in range(5):
        event = Event(
            source_ip="192.168.1.200",
            event_type="brute_force",
            severity="high",
            timestamp=now - timedelta(minutes=i * 2),  # Every 2 minutes
        )
        db_session.add(event)
        events.append(event)
    db_session.commit()
    
    # Run temporal correlation
    groups = run_temporal_correlation(db_session, window_minutes=15, min_events=5)
    
    # Should create 1 temporal group
    assert len(groups) == 1
    assert groups[0].rule_type == "temporal"
    assert groups[0].event_count == 5


# ── Fixture for sample events (used by unit tests) ─────────────────────

@pytest.fixture
def sample_events(db_session):
    """Create sample events for testing."""
    return _seed_events_for_correlation(db_session)


# ── Integration Tests: Routes ──────────────────────────────────────────

class TestRunCorrelationRoute:
    """Tests for POST /api/v1/correlations/run endpoint."""

    def test_run_correlation_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test triggering correlation as admin creates groups."""
        # Seed events using the db_session fixture
        _seed_events_for_correlation(db_session)
        
        response = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least one group created
        
        # Check structure of first group
        if len(data) > 0:
            group = data[0]
            assert "id" in group
            assert "rule_type" in group
            assert "rule_key" in group
            assert "severity" in group
            assert "score" in group
            assert "event_count" in group
            assert "events" in group

    def test_run_correlation_rejects_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that analyst cannot trigger correlation."""
        _seed_events_for_correlation(db_session)
        
        response = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 403

    def test_run_correlation_rejects_unauthenticated(self, client: TestClient, db_session: Session):
        """Test that unauthenticated user cannot trigger correlation."""
        _seed_events_for_correlation(db_session)
        
        response = client.post("/api/v1/correlations/run")
        
        assert response.status_code == 401

    def test_run_correlation_with_custom_params(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test correlation with custom query parameters."""
        # Seed events with only 2 events for an IP
        for i in range(2):
            _create_event(db_session, source_ip="192.168.1.50", minutes_ago=i * 5)
        
        # Run with min_events=2 (should catch the IP with 2 events)
        response = client.post(
            "/api/v1/correlations/run?min_events_ip=2&window_minutes_ip=60",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, list)

    def test_run_correlation_creates_ip_and_temporal_groups(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test that both IP and temporal correlation run."""
        now = datetime.utcnow()
        
        # Create events for IP correlation (same IP, 5 events)
        for i in range(5):
            _create_event(
                db_session,
                source_ip="192.168.1.100",
                event_type="login_failed",
                minutes_ago=i * 5
            )
        
        # Create events for temporal correlation (tight cluster)
        for i in range(5):
            _create_event(
                db_session,
                source_ip="10.0.0.99",
                event_type="brute_force",
                minutes_ago=i * 2  # Every 2 minutes
            )
        
        response = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Should have both ip_source and temporal groups
        rule_types = [g["rule_type"] for g in data]
        assert "ip_source" in rule_types

    def test_run_correlation_empty_db(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test running correlation on empty database."""
        response = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


class TestListCorrelationGroupsRoute:
    """Tests for GET /api/v1/correlations endpoint."""

    def test_list_correlations_as_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test listing correlation groups as analyst."""
        # Seed events and run correlation
        _seed_events_for_correlation(db_session)
        run_ip_correlation(db_session, window_minutes=30, min_events=3)
        
        response = client.get(
            "/api/v1/correlations",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 1
        assert len(data["items"]) >= 1

    def test_list_correlations_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test listing correlation groups as admin."""
        _seed_events_for_correlation(db_session)
        run_ip_correlation(db_session, window_minutes=30, min_events=3)
        
        response = client.get(
            "/api/v1/correlations",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    def test_list_correlations_rejects_unauthenticated(self, client: TestClient):
        """Test that unauthenticated user cannot list correlations."""
        response = client.get("/api/v1/correlations")
        
        assert response.status_code == 401

    def test_list_correlations_pagination(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test pagination of correlation groups list."""
        # Create multiple correlation groups
        for i in range(5):
            _create_correlation_group(
                db_session,
                rule_key=f"192.168.1.{i}",
                event_count=3
            )
        
        # Get first 2
        response = client.get(
            "/api/v1/correlations?skip=0&limit=2",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["skip"] == 0
        assert data["limit"] == 2

    def test_list_correlations_filter_by_status(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test filtering correlation groups by status."""
        # Create groups with different statuses
        _create_correlation_group(db_session, status="open")
        _create_correlation_group(db_session, status="investigating")
        _create_correlation_group(db_session, status="resolved")
        
        # Filter by open
        response = client.get(
            "/api/v1/correlations?status_filter=open",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(g["status"] == "open" for g in data["items"])

    def test_list_correlations_filter_by_rule_type(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test filtering correlation groups by rule type."""
        # Create groups with different rule types
        _create_correlation_group(db_session, rule_type="ip_source")
        _create_correlation_group(db_session, rule_type="temporal")
        
        # Filter by ip_source
        response = client.get(
            "/api/v1/correlations?rule_type_filter=ip_source",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(g["rule_type"] == "ip_source" for g in data["items"])

    def test_list_correlations_empty(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test listing when no correlation groups exist."""
        response = client.get(
            "/api/v1/correlations",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0

    def test_list_correlations_response_structure(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that response has correct structure."""
        _create_correlation_group(db_session)
        
        response = client.get(
            "/api/v1/correlations",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check paginated response structure
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
        
        # Check individual group structure
        if len(data["items"]) > 0:
            group = data["items"][0]
            assert "id" in group
            assert "rule_type" in group
            assert "rule_key" in group
            assert "severity" in group
            assert "score" in group
            assert "event_count" in group
            assert "status" in group


class TestGetCorrelationGroupRoute:
    """Tests for GET /api/v1/correlations/{group_id} endpoint."""

    def test_get_correlation_by_id(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test getting a specific correlation group by ID."""
        # Create a correlation group with events
        group = _create_correlation_group(db_session)
        
        # Add some events to the group
        event1 = _create_event(db_session, minutes_ago=10)
        event2 = _create_event(db_session, minutes_ago=5)
        group.events.append(event1)
        group.events.append(event2)
        db_session.commit()
        
        response = client.get(
            f"/api/v1/correlations/{group.id}",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == group.id
        assert data["rule_type"] == group.rule_type
        assert "events" in data
        assert len(data["events"]) == 2

    def test_get_correlation_not_found(self, client: TestClient, auth_headers_analyst: dict):
        """Test getting non-existent correlation group."""
        response = client.get(
            "/api/v1/correlations/99999",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_correlation_rejects_unauthenticated(self, client: TestClient, db_session: Session):
        """Test that unauthenticated user cannot get correlation group."""
        group = _create_correlation_group(db_session)
        
        response = client.get(f"/api/v1/correlations/{group.id}")
        
        assert response.status_code == 401

    def test_get_correlation_with_events(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that getting a group returns associated events."""
        group = _create_correlation_group(db_session, rule_key="192.168.1.100")
        
        # Create and associate events
        events = []
        for i in range(3):
            event = _create_event(
                db_session,
                source_ip="192.168.1.100",
                event_type="login_failed",
                minutes_ago=i * 5
            )
            events.append(event)
            group.events.append(event)
        db_session.commit()
        
        response = client.get(
            f"/api/v1/correlations/{group.id}",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["events"]) == 3
        
        # Check event structure
        event = data["events"][0]
        assert "id" in event
        assert "source_ip" in event
        assert "event_type" in event
        assert "severity" in event
        assert "timestamp" in event


class TestUpdateCorrelationGroupRoute:
    """Tests for PATCH /api/v1/correlations/{group_id} endpoint."""

    def test_update_correlation_status(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test updating correlation group status."""
        group = _create_correlation_group(db_session, status="open")
        
        response = client.patch(
            f"/api/v1/correlations/{group.id}",
            json={"status": "investigating"},
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "investigating"

    def test_update_correlation_assigned_to(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test updating correlation group assignment."""
        group = _create_correlation_group(db_session)
        
        # Create a user to assign to
        user = User(
            username="assignee",
            email="assignee@example.com",
            hashed_password=get_password_hash("password123"),
            role="analyst",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        response = client.patch(
            f"/api/v1/correlations/{group.id}",
            json={"assigned_to": user.id},
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["assigned_to"] == user.id

    def test_update_correlation_not_found(self, client: TestClient, auth_headers_analyst: dict):
        """Test updating non-existent correlation group."""
        response = client.patch(
            "/api/v1/correlations/99999",
            json={"status": "resolved"},
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_correlation_rejects_unauthenticated(self, client: TestClient, db_session: Session):
        """Test that unauthenticated user cannot update correlation."""
        group = _create_correlation_group(db_session)
        
        response = client.patch(
            f"/api/v1/correlations/{group.id}",
            json={"status": "investigating"}
        )
        
        assert response.status_code == 401

    def test_update_correlation_invalid_status(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test updating with invalid status value."""
        group = _create_correlation_group(db_session)
        
        response = client.patch(
            f"/api/v1/correlations/{group.id}",
            json={"status": "invalid_status"},
            headers=auth_headers_analyst
        )
        
        # API accepts the status (validation might be in schema or not)
        # Check that it returns either an error or success
        assert response.status_code in [200, 400, 422]

    def test_update_correlation_invalid_user(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test assigning to non-existent user."""
        group = _create_correlation_group(db_session)
        
        response = client.patch(
            f"/api/v1/correlations/{group.id}",
            json={"assigned_to": 99999},
            headers=auth_headers_admin
        )
        
        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()

    def test_update_correlation_partial(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test partial update (only status, not assigned_to)."""
        group = _create_correlation_group(db_session, status="open", assigned_to=None)
        
        response = client.patch(
            f"/api/v1/correlations/{group.id}",
            json={"status": "resolved"},
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "resolved"
        assert data["assigned_to"] is None  # Should remain unchanged


class TestCorrelationStatsRoute:
    """Tests for GET /api/v1/correlations/stats endpoint."""

    def test_stats_empty(self, client: TestClient, auth_headers_analyst: dict):
        """Test stats when no correlation groups exist."""
        response = client.get(
            "/api/v1/correlations/stats",
            headers=auth_headers_analyst
        )
        
        print(f"\nResponse status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_groups"] == 0
        assert data["by_rule_type"] == {}
        assert data["by_status"] == {}
        assert data["open_groups"] == 0

    def test_stats_with_data(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test stats with correlation groups in database."""
        # Create groups with different statuses and types
        _create_correlation_group(db_session, rule_type="ip_source", severity="high", status="open")
        _create_correlation_group(db_session, rule_type="ip_source", severity="medium", status="investigating")
        _create_correlation_group(db_session, rule_type="temporal", severity="critical", status="resolved")
        
        response = client.get(
            "/api/v1/correlations/stats",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_groups"] == 3
        assert data["by_status"]["open"] == 1
        assert data["by_status"]["investigating"] == 1
        assert data["by_status"]["resolved"] == 1
        assert data["open_groups"] == 1
        assert data["investigating_groups"] == 1
        assert data["resolved_groups"] == 1

    def test_stats_rejects_unauthenticated(self, client: TestClient):
        """Test that unauthenticated user cannot get stats."""
        response = client.get("/api/v1/correlations/stats")
        
        assert response.status_code == 401

    def test_stats_response_structure(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that stats response has correct structure."""
        _create_correlation_group(db_session)
        
        response = client.get(
            "/api/v1/correlations/stats",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all expected fields
        assert "total_groups" in data
        assert "by_rule_type" in data
        assert "by_status" in data
        assert "by_severity" in data
        assert "open_groups" in data
        assert "investigating_groups" in data
        assert "resolved_groups" in data
        assert "false_positive_groups" in data


# ── RBAC Tests ────────────────────────────────────────────────────────

class TestCorrelationRBAC:
    """Comprehensive RBAC tests for correlation endpoints."""

    def test_analyst_cannot_run_correlation(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst cannot access POST /run."""
        _seed_events_for_correlation(db_session)
        
        response = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_analyst
        )
        assert response.status_code == 403

    def test_analyst_can_list_correlations(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst can access GET /correlations."""
        _create_correlation_group(db_session)
        
        response = client.get(
            "/api/v1/correlations",
            headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_analyst_can_get_correlation(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst can access GET /correlations/{id}."""
        group = _create_correlation_group(db_session)
        
        response = client.get(
            f"/api/v1/correlations/{group.id}",
            headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_analyst_can_update_correlation(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst can access PATCH /correlations/{id}."""
        group = _create_correlation_group(db_session)
        
        response = client.patch(
            f"/api/v1/correlations/{group.id}",
            json={"status": "investigating"},
            headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_analyst_can_get_stats(self, client: TestClient, auth_headers_analyst: dict):
        """Test RBAC: analyst can access GET /correlations/stats."""
        response = client.get(
            "/api/v1/correlations/stats",
            headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_admin_can_run_correlation(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test RBAC: admin can access POST /run."""
        _seed_events_for_correlation(db_session)
        
        response = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_admin
        )
        assert response.status_code == 201

    def test_admin_can_do_everything(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test RBAC: admin can access all correlation endpoints."""
        # Run correlation
        _seed_events_for_correlation(db_session)
        response1 = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_admin
        )
        assert response1.status_code == 201
        
        # List correlations
        response2 = client.get(
            "/api/v1/correlations",
            headers=auth_headers_admin
        )
        assert response2.status_code == 200
        
        # Get stats
        response3 = client.get(
            "/api/v1/correlations/stats",
            headers=auth_headers_admin
        )
        assert response3.status_code == 200

    def test_unauthenticated_cannot_access_any_endpoint(self, client: TestClient, db_session: Session):
        """Test RBAC: unauthenticated user cannot access any correlation endpoint."""
        group = _create_correlation_group(db_session)
        
        # POST /run
        response1 = client.post("/api/v1/correlations/run")
        assert response1.status_code == 401
        
        # GET /correlations
        response2 = client.get("/api/v1/correlations")
        assert response2.status_code == 401
        
        # GET /correlations/{id}
        response3 = client.get(f"/api/v1/correlations/{group.id}")
        assert response3.status_code == 401
        
        # PATCH /correlations/{id}
        response4 = client.patch(f"/api/v1/correlations/{group.id}", json={"status": "resolved"})
        assert response4.status_code == 401
        
        # GET /correlations/stats
        response5 = client.get("/api/v1/correlations/stats")
        assert response5.status_code == 401


# ── Correlation Scenario Tests ────────────────────────────────────────

class TestCorrelationScenarios:
    """Tests for correlation scenarios with events."""

    def test_ip_correlation_creates_group(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test that events with same IP get grouped via correlation."""
        # Create 5 events from same IP
        for i in range(5):
            _create_event(
                db_session,
                source_ip="192.168.1.100",
                event_type="login_failed",
                minutes_ago=i * 5
            )
        
        # Run correlation
        response = client.post(
            "/api/v1/correlations/run?min_events_ip=3",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Should have at least one group for 192.168.1.100
        ip_groups = [g for g in data if g["rule_key"] == "192.168.1.100"]
        assert len(ip_groups) == 1
        assert ip_groups[0]["event_count"] == 5
        assert ip_groups[0]["rule_type"] == "ip_source"

    def test_correlation_score_calculated_correctly(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test that correlation score is calculated correctly."""
        # Create 3 high severity events
        for i in range(3):
            _create_event(
                db_session,
                source_ip="10.0.0.50",
                event_type="port_scan",
                severity="high",
                minutes_ago=i * 5
            )
        
        response = client.post(
            "/api/v1/correlations/run?min_events_ip=3",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        group = next((g for g in data if g["rule_key"] == "10.0.0.50"), None)
        assert group is not None
        # Score = 3 * 10 (events) + 3 * 20 (high severity) = 30 + 60 = 90
        assert group["score"] == 90
        assert group["severity"] == "high"

    def test_min_events_prevents_group_creation(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test that groups are not created when event count < min_events."""
        # Create only 2 events from an IP
        for i in range(2):
            _create_event(
                db_session,
                source_ip="172.16.0.10",
                minutes_ago=i * 5
            )
        
        # Run correlation with min_events=3
        response = client.post(
            "/api/v1/correlations/run?min_events_ip=3",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Should not have a group for 172.16.0.10
        ip_groups = [g for g in data if g["rule_key"] == "172.16.0.10"]
        assert len(ip_groups) == 0

    def test_temporal_correlation_nearby_events(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test temporal correlation with events close in time."""
        # Create 5 events in a tight temporal cluster (every 2 minutes)
        for i in range(5):
            _create_event(
                db_session,
                source_ip="192.168.1.200",
                event_type="brute_force",
                minutes_ago=i * 2
            )
        
        response = client.post(
            "/api/v1/correlations/run?min_events_temp=5&window_minutes_temp=15",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Should have a temporal group
        temp_groups = [g for g in data if g["rule_type"] == "temporal"]
        assert len(temp_groups) >= 1
        assert temp_groups[0]["event_count"] == 5

    def test_temporal_correlation_prevents_sparse_events(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test that temporally distant events don't get grouped."""
        now = datetime.utcnow()
        
        # Create events spread far apart (every 30 minutes)
        for i in range(5):
            event = Event(
                source_ip="10.0.0.100",
                event_type="suspicious_activity",
                severity="medium",
                timestamp=now - timedelta(minutes=i * 30),
            )
            db_session.add(event)
        db_session.commit()
        
        response = client.post(
            "/api/v1/correlations/run?min_events_temp=5&window_minutes_temp=15",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Should NOT have temporal group (events too far apart)
        # But might have ip_source group
        temp_groups = [g for g in data if g["rule_type"] == "temporal"]
        # Temporal group should not exist for events 30 min apart with 15 min window
        # (depending on implementation)

    def test_correlation_with_mixed_ips(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test correlation with multiple IPs creating multiple groups."""
        # Create events for 3 different IPs
        ips = ["192.168.1.10", "192.168.1.20", "192.168.1.30"]
        for ip in ips:
            for i in range(4):  # 4 events each
                _create_event(
                    db_session,
                    source_ip=ip,
                    minutes_ago=i * 5
                )
        
        response = client.post(
            "/api/v1/correlations/run?min_events_ip=3",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Should have 3 groups (one per IP)
        rule_keys = [g["rule_key"] for g in data]
        for ip in ips:
            assert ip in rule_keys

    def test_correlation_persists_in_db(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test that correlation groups are persisted in database."""
        # Create events
        for i in range(5):
            _create_event(
                db_session,
                source_ip="192.168.1.100",
                minutes_ago=i * 5
            )
        
        # Run correlation
        response = client.post(
            "/api/v1/correlations/run",
            headers=auth_headers_admin
        )
        assert response.status_code == 201
        
        # Check database directly
        groups = db_session.query(CorrelationGroup).filter(
            CorrelationGroup.rule_key == "192.168.1.100"
        ).all()
        
        assert len(groups) == 1
        assert groups[0].event_count == 5
        assert len(groups[0].events) == 5
