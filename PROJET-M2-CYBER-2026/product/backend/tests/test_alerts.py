"""Tests for alerts module.

Covers:
- Alert CRUD operations
- RBAC (admin-only create, analyst/admin read)
- Filtering and pagination
- Status updates
- Statistics endpoint
- Audit trail integration
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.audit import AuditLog


# ── Helpers ──────────────────────────────────────────────────────────────

def _create_alert_payload(title="Test Alert", severity="high", description="Test description", source_event_id=None):
    payload = {"title": title, "severity": severity, "description": description}
    if source_event_id:
        payload["source_event_id"] = source_event_id
    return payload


# ── POST /api/v1/alerts — create ─────────────────────────────────────────

class TestCreateAlert:
    def test_create_alert_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        payload = _create_alert_payload()
        response = client.post("/api/v1/alerts", json=payload, headers=auth_headers_admin)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Alert"
        assert data["severity"] == "high"
        assert data["status"] == "new"
        assert data["id"] is not None

    def test_create_alert_rejects_analyst(self, client: TestClient, auth_headers_analyst: dict):
        payload = _create_alert_payload()
        response = client.post("/api/v1/alerts", json=payload, headers=auth_headers_analyst)
        assert response.status_code == 403

    def test_create_alert_rejects_unauthenticated(self, client: TestClient):
        payload = _create_alert_payload()
        response = client.post("/api/v1/alerts", json=payload)
        assert response.status_code == 401

    def test_create_alert_with_source_event(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        payload = _create_alert_payload(source_event_id="evt-123")
        response = client.post("/api/v1/alerts", json=payload, headers=auth_headers_admin)
        assert response.status_code == 201
        assert response.json()["source_event_id"] == "evt-123"

    def test_create_alert_validates_title_max_length(self, client: TestClient, auth_headers_admin: dict):
        payload = _create_alert_payload(title="A" * 256)
        response = client.post("/api/v1/alerts", json=payload, headers=auth_headers_admin)
        assert response.status_code == 422

    def test_create_alert_validates_severity_enum(self, client: TestClient, auth_headers_admin: dict):
        payload = _create_alert_payload(severity="extreme")
        response = client.post("/api/v1/alerts", json=payload, headers=auth_headers_admin)
        assert response.status_code == 422

    def test_create_alert_writes_audit_log(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        payload = _create_alert_payload()
        client.post("/api/v1/alerts", json=payload, headers=auth_headers_admin)
        audit_entry = db_session.query(AuditLog).filter(AuditLog.action == "alert_created").first()
        assert audit_entry is not None
        assert audit_entry.resource_type == "alert"


# ── GET /api/v1/alerts — list ────────────────────────────────────────────

class TestListAlerts:
    def _seed_alerts(self, db_session: Session):
        for i in range(5):
            alert = Alert(
                title=f"Alert {i}",
                description=f"Description {i}",
                severity="low" if i % 2 == 0 else "high",
                status="new" if i < 3 else "resolved",
            )
            db_session.add(alert)
        db_session.commit()

    def test_list_alerts_as_analyst(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        self._seed_alerts(db_session)
        response = client.get("/api/v1/alerts", headers=auth_headers_analyst)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 5

    def test_list_alerts_pagination(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        self._seed_alerts(db_session)
        response = client.get("/api/v1/alerts?skip=2&limit=2", headers=auth_headers_analyst)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["skip"] == 2
        assert data["limit"] == 2

    def test_list_alerts_filter_by_status(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        self._seed_alerts(db_session)
        response = client.get("/api/v1/alerts?status_filter=resolved", headers=auth_headers_analyst)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert all(a["status"] == "resolved" for a in data["items"])

    def test_list_alerts_filter_by_severity(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        self._seed_alerts(db_session)
        response = client.get("/api/v1/alerts?severity_filter=high", headers=auth_headers_analyst)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert all(a["severity"] == "high" for a in data["items"])

    def test_list_alerts_rejects_unauthenticated(self, client: TestClient):
        response = client.get("/api/v1/alerts")
        assert response.status_code == 401


# ── GET /api/v1/alerts/{alert_id} — detail ───────────────────────────────

class TestGetAlert:
    def test_get_alert_by_id(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        alert = Alert(title="Detail Alert", description="Desc", severity="critical", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        response = client.get(f"/api/v1/alerts/{alert.id}", headers=auth_headers_analyst)
        assert response.status_code == 200
        assert response.json()["title"] == "Detail Alert"

    def test_get_alert_not_found(self, client: TestClient, auth_headers_analyst: dict):
        response = client.get("/api/v1/alerts/99999", headers=auth_headers_analyst)
        assert response.status_code == 404


# ── PATCH /api/v1/alerts/{alert_id}/status — update ──────────────────────

class TestUpdateAlertStatus:
    def test_update_status_to_investigating(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        alert = Alert(title="Status Alert", description="Desc", severity="medium", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        response = client.patch(
            f"/api/v1/alerts/{alert.id}/status",
            json={"status": "investigating"},
            headers=auth_headers_analyst,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "investigating"
        assert response.json()["resolved_at"] is None

    def test_update_status_to_resolved_sets_resolved_at(
        self, client: TestClient, auth_headers_analyst: dict, db_session: Session
    ):
        alert = Alert(title="Resolve Alert", description="Desc", severity="high", status="investigating")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        response = client.patch(
            f"/api/v1/alerts/{alert.id}/status",
            json={"status": "resolved"},
            headers=auth_headers_analyst,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"
        assert response.json()["resolved_at"] is not None

    def test_update_status_to_false_positive_sets_resolved_at(
        self, client: TestClient, auth_headers_admin: dict, db_session: Session
    ):
        alert = Alert(title="FP Alert", description="Desc", severity="low", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        response = client.patch(
            f"/api/v1/alerts/{alert.id}/status",
            json={"status": "false_positive"},
            headers=auth_headers_admin,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "false_positive"
        assert response.json()["resolved_at"] is not None

    def test_update_alert_not_found(self, client: TestClient, auth_headers_analyst: dict):
        response = client.patch(
            "/api/v1/alerts/99999/status",
            json={"status": "resolved"},
            headers=auth_headers_analyst,
        )
        assert response.status_code == 404

    def test_update_status_writes_audit_log(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        alert = Alert(title="Audit Alert", description="Desc", severity="medium", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        client.patch(
            f"/api/v1/alerts/{alert.id}/status",
            json={"status": "investigating"},
            headers=auth_headers_analyst,
        )
        audit_entry = db_session.query(AuditLog).filter(AuditLog.action == "alert_status_updated").first()
        assert audit_entry is not None
        assert audit_entry.resource_id == str(alert.id)


# ── GET /api/v1/alerts/stats — statistics ────────────────────────────────

class TestAlertStats:
    def test_stats_empty(self, client: TestClient, auth_headers_analyst: dict):
        response = client.get("/api/v1/alerts/stats", headers=auth_headers_analyst)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["by_status"] == {}
        assert data["by_severity"] == {}

    def test_stats_with_data(self, client: TestClient, auth_headers_analyst: dict, db_session: Session):
        for sev in ["low", "medium", "high", "critical"]:
            db_session.add(Alert(title=f"Stat {sev}", description="D", severity=sev, status="new"))
        db_session.add(Alert(title="Resolved", description="D", severity="high", status="resolved"))
        db_session.commit()

        response = client.get("/api/v1/alerts/stats", headers=auth_headers_analyst)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert data["by_severity"]["high"] == 2
        assert data["by_status"]["new"] == 4
        assert data["by_status"]["resolved"] == 1

    def test_stats_rejects_unauthenticated(self, client: TestClient):
        response = client.get("/api/v1/alerts/stats")
        assert response.status_code == 401


# ── POST /api/v1/alerts/{alert_id}/assign — assign alert ─────────────────

class TestAssignAlert:
    """Tests for alert assignment functionality."""

    def test_assign_alert_as_admin_success(
        self, client: TestClient, auth_headers_admin: dict, auth_headers_analyst: dict,
        db_session: Session
    ):
        """Test that admin can assign an alert to an analyst."""
        # Create an alert
        alert = Alert(title="Assign Test", description="Desc", severity="high", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        # Get analyst user ID
        from app.models.user import User
        analyst = db_session.query(User).filter(User.role == "analyst").first()

        # Assign alert to analyst
        response = client.post(
            f"/api/v1/alerts/{alert.id}/assign",
            json={"user_id": analyst.id},
            headers=auth_headers_admin,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["assigned_to"] == analyst.id

    def test_assign_alert_rejects_analyst(
        self, client: TestClient, auth_headers_analyst: dict, db_session: Session
    ):
        """Test that analyst cannot assign alerts (admin only)."""
        alert = Alert(title="Analyst Assign", description="Desc", severity="medium", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        response = client.post(
            f"/api/v1/alerts/{alert.id}/assign",
            json={"user_id": 1},
            headers=auth_headers_analyst,
        )
        assert response.status_code == 403

    def test_assign_alert_to_valid_analyst(
        self, client: TestClient, auth_headers_admin: dict, db_session: Session
    ):
        """Test assigning alert to a valid analyst."""
        # Create alert
        alert = Alert(title="Valid Analyst", description="Desc", severity="low", status="new")
        db_session.add(alert)

        # Create another analyst
        from app.models.user import User
        from app.auth.service import get_password_hash
        analyst = User(
            username="analyst2",
            email="analyst2@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Analyst 2",
            role="analyst",
            is_active=True,
        )
        db_session.add(analyst)
        db_session.commit()
        db_session.refresh(alert)
        db_session.refresh(analyst)

        # Assign to analyst
        response = client.post(
            f"/api/v1/alerts/{alert.id}/assign",
            json={"user_id": analyst.id},
            headers=auth_headers_admin,
        )
        assert response.status_code == 200
        assert response.json()["assigned_to"] == analyst.id

    def test_assign_alert_to_nonexistent_user(
        self, client: TestClient, auth_headers_admin: dict, db_session: Session
    ):
        """Test assigning alert to a non-existent user returns 400."""
        alert = Alert(title="Nonexistent User", description="Desc", severity="critical", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        response = client.post(
            f"/api/v1/alerts/{alert.id}/assign",
            json={"user_id": 99999},
            headers=auth_headers_admin,
        )
        assert response.status_code == 400
        assert "Invalid user" in response.json()["detail"]

    def test_assign_alert_to_non_analyst_user(
        self, client: TestClient, auth_headers_admin: dict, db_session: Session
    ):
        """Test assigning alert to a user who is not an analyst/admin returns 400."""
        # Create alert
        alert = Alert(title="Non Analyst", description="Desc", severity="high", status="new")
        db_session.add(alert)

        # Create a user with invalid role (simulate by creating and checking)
        # Since role field accepts string, we'll test with a non-analyst role
        from app.models.user import User
        from app.auth.service import get_password_hash
        regular_user = User(
            username="regular",
            email="regular@test.com",
            hashed_password=get_password_hash("password123"),
            full_name="Regular User",
            role="user",  # Not analyst or admin
            is_active=True,
        )
        db_session.add(regular_user)
        db_session.commit()
        db_session.refresh(alert)
        db_session.refresh(regular_user)

        response = client.post(
            f"/api/v1/alerts/{alert.id}/assign",
            json={"user_id": regular_user.id},
            headers=auth_headers_admin,
        )
        assert response.status_code == 400
        assert "not an analyst" in response.json()["detail"]

    def test_assign_nonexistent_alert(
        self, client: TestClient, auth_headers_admin: dict, db_session: Session, test_user_analyst
    ):
        """Test assigning a non-existent alert returns 404."""
        response = client.post(
            "/api/v1/alerts/99999/assign",
            json={"user_id": test_user_analyst.id},
            headers=auth_headers_admin,
        )
        assert response.status_code == 404
        assert "Alert not found" in response.json()["detail"]

    def test_assign_alert_writes_audit_log(
        self, client: TestClient, auth_headers_admin: dict, db_session: Session, test_user_analyst
    ):
        """Test that assigning an alert writes an audit log entry."""
        # Create alert
        alert = Alert(title="Audit Assign", description="Desc", severity="medium", status="new")
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        # Assign alert to analyst
        client.post(
            f"/api/v1/alerts/{alert.id}/assign",
            json={"user_id": test_user_analyst.id},
            headers=auth_headers_admin,
        )

        # Check audit log
        from app.models.audit import AuditLog
        audit_entry = db_session.query(AuditLog).filter(AuditLog.action == "alert_assigned").first()
        assert audit_entry is not None
        assert audit_entry.resource_type == "alert"
        assert audit_entry.resource_id == str(alert.id)
