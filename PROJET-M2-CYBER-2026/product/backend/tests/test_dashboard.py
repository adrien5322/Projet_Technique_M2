"""Tests for dashboard module.

Covers:
- Dashboard service functions (summary, attackers, activity timeline)
- Dashboard API endpoints (RBAC, parameters, response structure)
- UI pages (HTML responses, authentication)
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import List

from app.models.event import Event
from app.models.alert import Alert
from app.models.asset import Asset
from app.models.correlation import CorrelationGroup
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


def _create_alert(db_session: Session, title: str = "Test Alert",
                  severity: str = "high", status: str = "new",
                  minutes_ago: int = 0) -> Alert:
    """Helper to create an alert in the database."""
    alert = Alert(
        title=title,
        description="Test description",
        severity=severity,
        status=status,
        created_at=datetime.utcnow() - timedelta(minutes=minutes_ago),
    )
    db_session.add(alert)
    db_session.commit()
    db_session.refresh(alert)
    return alert


def _create_asset(db_session: Session, ip_address: str = "192.168.1.10",
                  hostname: str = "server-01") -> Asset:
    """Helper to create an asset in the database."""
    asset = Asset(
        ip_address=ip_address,
        hostname=hostname,
        os="Linux",
        status="active",
    )
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)
    return asset


def _create_correlation_group(db_session: Session, rule_type: str = "ip_source",
                              rule_key: str = "192.168.1.100", severity: str = "medium",
                              score: int = 50, event_count: int = 3) -> CorrelationGroup:
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
        status="open",
        description=f"Test correlation group for {rule_key}",
    )
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)
    return group


def _seed_dashboard_data(db_session: Session) -> dict:
    """Create sample data for dashboard testing."""
    data = {}
    
    # Create assets
    data['asset1'] = _create_asset(db_session, "192.168.1.10", "web-server")
    data['asset2'] = _create_asset(db_session, "192.168.1.20", "db-server")
    data['asset3'] = _create_asset(db_session, "10.0.0.50", "workstation-01")
    
    # Create events from different IPs
    for i in range(5):
        _create_event(db_session, source_ip="192.168.1.100", 
                     event_type="login_failed", severity="medium",
                     minutes_ago=i*10)
    
    for i in range(3):
        _create_event(db_session, source_ip="10.0.0.50", 
                     event_type="port_scan", severity="high",
                     minutes_ago=i*5)
    
    # Create alerts
    data['alert1'] = _create_alert(db_session, "Critical Alert", "critical", "new", 10)
    data['alert2'] = _create_alert(db_session, "High Alert", "high", "investigating", 20)
    data['alert3'] = _create_alert(db_session, "Medium Alert", "medium", "resolved", 30)
    
    # Create correlation groups
    data['correlation1'] = _create_correlation_group(
        db_session, "ip_source", "192.168.1.100", "medium", 60, 5
    )
    data['correlation2'] = _create_correlation_group(
        db_session, "ip_source", "10.0.0.50", "high", 80, 3
    )
    
    return data


# ── Service Tests (Unit Tests) ─────────────────────────────────────────

@pytest.mark.skip(reason="Dashboard service not yet implemented")
class TestDashboardService:
    """Tests for dashboard service functions."""
    
    def test_get_dashboard_summary_empty_db(self, db_session: Session):
        """Test get_dashboard_summary with empty database."""
        from app.dashboard.service import get_dashboard_summary
        
        summary = get_dashboard_summary(db_session)
        
        assert summary["total_events"] == 0
        assert summary["total_alerts"] == 0
        assert summary["open_alerts"] == 0
        assert summary["total_assets"] == 0
        assert summary["active_assets"] == 0
        assert summary["total_correlations"] == 0
        assert summary["open_correlations"] == 0
    
    def test_get_dashboard_summary_with_data(self, db_session: Session):
        """Test get_dashboard_summary with data in database."""
        from app.dashboard.service import get_dashboard_summary
        
        _seed_dashboard_data(db_session)
        
        summary = get_dashboard_summary(db_session)
        
        assert summary["total_events"] == 8  # 5 + 3
        assert summary["total_alerts"] == 3
        assert summary["open_alerts"] == 2  # new + investigating
        assert summary["total_assets"] == 3
        assert summary["active_assets"] == 3
        assert summary["total_correlations"] == 2
        assert summary["open_correlations"] == 2
    
    def test_get_top_attackers_sorted_by_score(self, db_session: Session):
        """Test get_top_attackers returns attackers sorted by score."""
        from app.dashboard.service import get_top_attackers
        
        _seed_dashboard_data(db_session)
        
        attackers = get_top_attackers(db_session, limit=10)
        
        assert len(attackers) >= 2
        # Check that attackers are sorted by score descending
        for i in range(len(attackers) - 1):
            assert attackers[i]["score"] >= attackers[i + 1]["score"]
    
    def test_get_top_attackers_score_calculated_correctly(self, db_session: Session):
        """Test that attacker score is calculated correctly."""
        from app.dashboard.service import get_top_attackers
        
        # Create events with known pattern
        for i in range(5):
            _create_event(db_session, source_ip="192.168.1.100", 
                         event_type="login_failed", severity="high",
                         minutes_ago=i*5)
        
        attackers = get_top_attackers(db_session, limit=10)
        
        # Find our IP in the results
        attacker = next((a for a in attackers if a["ip"] == "192.168.1.100"), None)
        assert attacker is not None
        assert attacker["event_count"] == 5
        assert attacker["score"] > 0  # Score should be calculated
    
    def test_get_top_attackers_limit_works(self, db_session: Session):
        """Test that limit parameter works correctly."""
        from app.dashboard.service import get_top_attackers
        
        # Create multiple IPs with events
        for ip_idx in range(5):
            ip = f"10.0.0.{ip_idx}"
            for i in range(3):
                _create_event(db_session, source_ip=ip, 
                             event_type="login_failed", severity="medium",
                             minutes_ago=i*5)
        
        attackers = get_top_attackers(db_session, limit=3)
        
        assert len(attackers) == 3
    
    def test_get_activity_timeline_default_24h(self, db_session: Session):
        """Test get_activity_timeline uses 24h default."""
        from app.dashboard.service import get_activity_timeline
        
        # Create events within last 24h
        for i in range(5):
            _create_event(db_session, minutes_ago=i*60)  # Every hour
        
        # Create event older than 24h
        old_event = Event(
            source_ip="192.168.1.200",
            event_type="old_event",
            severity="low",
            timestamp=datetime.utcnow() - timedelta(hours=25),
        )
        db_session.add(old_event)
        db_session.commit()
        
        timeline = get_activity_timeline(db_session)
        
        # Should only include events from last 24h
        assert len(timeline) >= 1
        # Check that all events are within 24h
        for entry in timeline:
            event_time = datetime.fromisoformat(entry["hour"].replace("Z", "+00:00"))
            assert datetime.utcnow() - event_time <= timedelta(hours=24)
    
    def test_get_activity_timeline_with_hours_param(self, db_session: Session):
        """Test get_activity_timeline with custom hours parameter."""
        from app.dashboard.service import get_activity_timeline
        
        # Create events within last 6h
        for i in range(3):
            _create_event(db_session, minutes_ago=i*30)  # Every 30 min in last 1.5h
        
        # Create event 12h ago
        old_event = Event(
            source_ip="192.168.1.200",
            event_type="old_event",
            severity="low",
            timestamp=datetime.utcnow() - timedelta(hours=12),
        )
        db_session.add(old_event)
        db_session.commit()
        
        # Request only last 6 hours
        timeline = get_activity_timeline(db_session, hours=6)
        
        # Should not include the 12h old event
        assert len(timeline) >= 1
        for entry in timeline:
            event_time = datetime.fromisoformat(entry["hour"].replace("Z", "+00:00"))
            assert datetime.utcnow() - event_time <= timedelta(hours=6)
    
    def test_get_activity_timeline_returns_hours(self, db_session: Session):
        """Test that activity timeline returns proper hour buckets."""
        from app.dashboard.service import get_activity_timeline
        
        # Create events in specific hours
        now = datetime.utcnow()
        for hour_offset in [0, 1, 2]:  # 0h ago, 1h ago, 2h ago
            event_time = now - timedelta(hours=hour_offset)
            event = Event(
                source_ip="192.168.1.100",
                event_type="test_event",
                severity="low",
                timestamp=event_time,
            )
            db_session.add(event)
        db_session.commit()
        
        timeline = get_activity_timeline(db_session, hours=3)
        
        assert len(timeline) == 3
        # Check structure of each entry
        for entry in timeline:
            assert "hour" in entry
            assert "count" in entry
            assert isinstance(entry["count"], int)
            assert entry["count"] >= 0


# ── API Route Tests ─────────────────────────────────────────────────────

@pytest.mark.skip(reason="Dashboard routes not yet implemented")
class TestDashboardSummaryRoute:
    """Tests for GET /api/v1/dashboard/summary endpoint."""
    
    def test_get_summary_as_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test getting dashboard summary as analyst."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/summary",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "total_events" in data
        assert "total_alerts" in data
        assert "open_alerts" in data
        assert "total_assets" in data
        assert "active_assets" in data
        assert "total_correlations" in data
        assert "open_correlations" in data
    
    def test_get_summary_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test getting dashboard summary as admin."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/summary",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_events"] >= 0
    
    def test_get_summary_rejects_unauthenticated(self, client: TestClient, db_session: Session):
        """Test that unauthenticated user cannot get dashboard summary."""
        response = client.get("/api/v1/dashboard/summary")
        
        assert response.status_code == 401
    
    def test_get_summary_empty_db(self, client: TestClient, auth_headers_analyst: dict):
        """Test dashboard summary with empty database."""
        response = client.get(
            "/api/v1/dashboard/summary",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_events"] == 0
        assert data["total_alerts"] == 0


@pytest.mark.skip(reason="Dashboard routes not yet implemented")
class TestDashboardAttackersRoute:
    """Tests for GET /api/v1/dashboard/attackers endpoint."""
    
    def test_get_attackers_as_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test getting top attackers as analyst."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/attackers",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        if len(data) > 0:
            attacker = data[0]
            assert "ip" in attacker
            assert "event_count" in attacker
            assert "score" in attacker
    
    def test_get_attackers_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test getting top attackers as admin."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/attackers",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_attackers_with_limit_param(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test getting top attackers with limit parameter."""
        # Create multiple attackers
        for ip_idx in range(5):
            ip = f"10.0.0.{ip_idx}"
            for i in range(3):
                _create_event(db_session, source_ip=ip, minutes_ago=i*5)
        
        response = client.get(
            "/api/v1/dashboard/attackers?limit=3",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3
    
    def test_get_attackers_rejects_unauthenticated(self, client: TestClient):
        """Test that unauthenticated user cannot get attackers list."""
        response = client.get("/api/v1/dashboard/attackers")
        
        assert response.status_code == 401
    
    def test_get_attackers_sorted_by_score(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that attackers are sorted by score descending."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/attackers",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["score"] >= data[i + 1]["score"]


@pytest.mark.skip(reason="Dashboard routes not yet implemented")
class TestDashboardActivityRoute:
    """Tests for GET /api/v1/dashboard/activity endpoint."""
    
    def test_get_activity_as_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test getting activity timeline as analyst."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/activity",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        if len(data) > 0:
            entry = data[0]
            assert "hour" in entry
            assert "count" in entry
    
    def test_get_activity_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        """Test getting activity timeline as admin."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/activity",
            headers=auth_headers_admin
        )
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_activity_with_hours_param(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test getting activity timeline with custom hours parameter."""
        # Create some events
        for i in range(5):
            _create_event(db_session, minutes_ago=i*30)
        
        response = client.get(
            "/api/v1/dashboard/activity?hours=6",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_activity_rejects_unauthenticated(self, client: TestClient):
        """Test that unauthenticated user cannot get activity timeline."""
        response = client.get("/api/v1/dashboard/activity")
        
        assert response.status_code == 401
    
    def test_get_activity_default_24h(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that activity defaults to 24 hours."""
        # Create recent events
        for i in range(3):
            _create_event(db_session, minutes_ago=i*30)
        
        response = client.get(
            "/api/v1/dashboard/activity",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        # Should return timeline data
        assert isinstance(data, list)


# ── UI Page Tests ──────────────────────────────────────────────────────

@pytest.mark.skip(reason="UI pages not yet implemented")
class TestDashboardUIPages:
    """Tests for UI pages served by FastAPI."""
    
    def test_dashboard_page_requires_auth(self, client: TestClient):
        """Test that dashboard page requires authentication."""
        response = client.get("/")
        
        # Should redirect to login or return 401
        assert response.status_code in [302, 401, 403]
    
    def test_dashboard_page_with_auth(self, client: TestClient, auth_headers_analyst: dict):
        """Test that dashboard page returns HTML with authentication."""
        response = client.get("/", headers=auth_headers_analyst)
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        # Check for some HTML content
        assert "<html" in response.text.lower() or "<!doctype" in response.text.lower()
    
    def test_assets_page_with_auth(self, client: TestClient, auth_headers_analyst: dict):
        """Test that assets page returns HTML with authentication."""
        response = client.get("/assets", headers=auth_headers_analyst)
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_events_page_with_auth(self, client: TestClient, auth_headers_analyst: dict):
        """Test that events page returns HTML with authentication."""
        response = client.get("/events", headers=auth_headers_analyst)
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_alerts_page_with_auth(self, client: TestClient, auth_headers_analyst: dict):
        """Test that alerts page returns HTML with authentication."""
        response = client.get("/alerts", headers=auth_headers_analyst)
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_attackers_page_with_auth(self, client: TestClient, auth_headers_analyst: dict):
        """Test that attackers page returns HTML with authentication."""
        response = client.get("/attackers", headers=auth_headers_analyst)
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_login_page_without_auth(self, client: TestClient):
        """Test that login page is accessible without authentication."""
        response = client.get("/login")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_assets_page_rejects_unauthenticated(self, client: TestClient):
        """Test that assets page rejects unauthenticated users."""
        response = client.get("/assets")
        
        assert response.status_code in [302, 401, 403]
    
    def test_events_page_rejects_unauthenticated(self, client: TestClient):
        """Test that events page rejects unauthenticated users."""
        response = client.get("/events")
        
        assert response.status_code in [302, 401, 403]
    
    def test_alerts_page_rejects_unauthenticated(self, client: TestClient):
        """Test that alerts page rejects unauthenticated users."""
        response = client.get("/alerts")
        
        assert response.status_code in [302, 401, 403]
    
    def test_attackers_page_rejects_unauthenticated(self, client: TestClient):
        """Test that attackers page rejects unauthenticated users."""
        response = client.get("/attackers")
        
        assert response.status_code in [302, 401, 403]


# ── RBAC Tests ─────────────────────────────────────────────────────────

@pytest.mark.skip(reason="Dashboard routes not yet implemented")
class TestDashboardRBAC:
    """Comprehensive RBAC tests for dashboard endpoints."""
    
    def test_analyst_can_access_summary(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst can access GET /api/v1/dashboard/summary."""
        response = client.get(
            "/api/v1/dashboard/summary",
            headers=auth_headers_analyst
        )
        assert response.status_code == 200
    
    def test_admin_can_access_summary(self, client: TestClient, auth_headers_admin: dict):
        """Test RBAC: admin can access GET /api/v1/dashboard/summary."""
        response = client.get(
            "/api/v1/dashboard/summary",
            headers=auth_headers_admin
        )
        assert response.status_code == 200
    
    def test_analyst_can_access_attackers(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst can access GET /api/v1/dashboard/attackers."""
        response = client.get(
            "/api/v1/dashboard/attackers",
            headers=auth_headers_analyst
        )
        assert response.status_code == 200
    
    def test_admin_can_access_attackers(self, client: TestClient, auth_headers_admin: dict):
        """Test RBAC: admin can access GET /api/v1/dashboard/attackers."""
        response = client.get(
            "/api/v1/dashboard/attackers",
            headers=auth_headers_admin
        )
        assert response.status_code == 200
    
    def test_analyst_can_access_activity(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test RBAC: analyst can access GET /api/v1/dashboard/activity."""
        response = client.get(
            "/api/v1/dashboard/activity",
            headers=auth_headers_analyst
        )
        assert response.status_code == 200
    
    def test_admin_can_access_activity(self, client: TestClient, auth_headers_admin: dict):
        """Test RBAC: admin can access GET /api/v1/dashboard/activity."""
        response = client.get(
            "/api/v1/dashboard/activity",
            headers=auth_headers_admin
        )
        assert response.status_code == 200
    
    def test_unauthenticated_cannot_access_summary(self, client: TestClient):
        """Test RBAC: unauthenticated user cannot access summary."""
        response = client.get("/api/v1/dashboard/summary")
        assert response.status_code == 401
    
    def test_unauthenticated_cannot_access_attackers(self, client: TestClient):
        """Test RBAC: unauthenticated user cannot access attackers."""
        response = client.get("/api/v1/dashboard/attackers")
        assert response.status_code == 401
    
    def test_unauthenticated_cannot_access_activity(self, client: TestClient):
        """Test RBAC: unauthenticated user cannot access activity."""
        response = client.get("/api/v1/dashboard/activity")
        assert response.status_code == 401
    
    def test_inactive_user_cannot_access_dashboard(self, client: TestClient, test_user_inactive, db_session: Session):
        """Test RBAC: inactive user cannot access dashboard endpoints."""
        from app.auth.service import create_access_token
        
        token = create_access_token({
            "sub": test_user_inactive.username,
            "role": test_user_inactive.role
        })
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/api/v1/dashboard/summary", headers=headers)
        assert response.status_code in [401, 403]


# ── Integration Tests ───────────────────────────────────────────────────

@pytest.mark.skip(reason="Dashboard routes not yet implemented")
class TestDashboardIntegration:
    """Integration tests for dashboard functionality."""
    
    def test_summary_matches_actual_counts(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that summary endpoint returns accurate counts."""
        # Seed specific data
        for i in range(5):
            _create_event(db_session, minutes_ago=i*10)
        
        _create_alert(db_session, "Test Alert 1", "high", "new")
        _create_alert(db_session, "Test Alert 2", "medium", "resolved")
        
        response = client.get(
            "/api/v1/dashboard/summary",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify counts match actual data
        assert data["total_events"] == 5
        assert data["total_alerts"] == 2
        assert data["open_alerts"] == 1  # Only the "new" one
    
    def test_attackers_returns_valid_json(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that attackers endpoint returns valid JSON structure."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/attackers",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate structure of each attacker
        for attacker in data:
            assert "ip" in attacker
            assert "event_count" in attacker
            assert "score" in attacker
            assert isinstance(attacker["ip"], str)
            assert isinstance(attacker["event_count"], int)
            assert isinstance(attacker["score"], int)
    
    def test_activity_returns_valid_json(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        """Test that activity endpoint returns valid JSON structure."""
        _seed_dashboard_data(db_session)
        
        response = client.get(
            "/api/v1/dashboard/activity",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate structure of each timeline entry
        for entry in data:
            assert "hour" in entry
            assert "count" in entry
            assert isinstance(entry["hour"], str)
            assert isinstance(entry["count"], int)
            assert entry["count"] >= 0
