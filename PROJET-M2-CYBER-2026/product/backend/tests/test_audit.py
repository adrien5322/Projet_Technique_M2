"""Tests for audit module.

Covers:
- Audit log creation (internal endpoint)
- Audit log listing with filters (admin only)
- Pagination
- RBAC enforcement
- Login audit trail integration
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.user import User


# ── Helpers ──────────────────────────────────────────────────────────────

def _audit_log_payload(action="test_action", resource_type="test", user_id=None, details=None, ip_address=None):
    payload = {"action": action, "resource_type": resource_type}
    if user_id is not None:
        payload["user_id"] = user_id
    if details is not None:
        payload["details"] = details
    if ip_address is not None:
        payload["ip_address"] = ip_address
    return payload


# ── POST /api/v1/audit/log — create (internal) ───────────────────────────

class TestCreateAuditLog:
    def test_create_audit_log_with_agent_secret(self, client: TestClient, db_session: Session, agent_secret_headers: dict):
        """Internal endpoint requires agent secret."""
        payload = _audit_log_payload()
        response = client.post("/api/v1/audit/log", json=payload, headers=agent_secret_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["action"] == "test_action"
        assert data["resource_type"] == "test"

    def test_create_audit_log_rejects_no_auth(self, client: TestClient, db_session: Session):
        """Internal endpoint must reject unauthenticated requests."""
        payload = _audit_log_payload()
        response = client.post("/api/v1/audit/log", json=payload)
        assert response.status_code == 401

    def test_create_audit_log_with_all_fields(self, client: TestClient, db_session: Session, agent_secret_headers: dict):
        payload = _audit_log_payload(
            action="user_login",
            resource_type="user",
            user_id=1,
            details={"username": "testuser"},
            ip_address="192.168.1.100",
        )
        response = client.post("/api/v1/audit/log", json=payload, headers=agent_secret_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == 1
        assert data["details"] == {"username": "testuser"}
        assert data["ip_address"] == "192.168.1.100"

    def test_create_audit_log_validates_action_max_length(self, client: TestClient, agent_secret_headers: dict):
        payload = _audit_log_payload(action="A" * 101)
        response = client.post("/api/v1/audit/log", json=payload, headers=agent_secret_headers)
        assert response.status_code == 422


# ── GET /api/v1/audit/logs — list ────────────────────────────────────────

class TestListAuditLogs:
    def _seed_logs(self, db_session: Session):
        for i in range(6):
            log = AuditLog(
                action="login_success" if i % 2 == 0 else "alert_created",
                resource_type="user" if i % 2 == 0 else "alert",
                resource_id=str(i),
                user_id=1 if i < 4 else 2,
                details={"index": i},
                ip_address=f"10.0.0.{i}",
            )
            db_session.add(log)
        db_session.commit()

    def test_list_logs_as_admin(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        self._seed_logs(db_session)
        response = client.get("/api/v1/audit/logs", headers=auth_headers_admin)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 6
        assert len(data["items"]) == 6

    def test_list_logs_rejects_analyst(self, client: TestClient, auth_headers_analyst: dict):
        response = client.get("/api/v1/audit/logs", headers=auth_headers_analyst)
        assert response.status_code == 403

    def test_list_logs_rejects_unauthenticated(self, client: TestClient):
        response = client.get("/api/v1/audit/logs")
        assert response.status_code == 401

    def test_list_logs_pagination(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        self._seed_logs(db_session)
        response = client.get("/api/v1/audit/logs?skip=2&limit=3", headers=auth_headers_admin)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 6
        assert len(data["items"]) == 3
        assert data["skip"] == 2
        assert data["limit"] == 3

    def test_list_logs_filter_by_action(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        self._seed_logs(db_session)
        response = client.get("/api/v1/audit/logs?action_filter=login_success", headers=auth_headers_admin)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert all(log["action"] == "login_success" for log in data["items"])

    def test_list_logs_filter_by_user_id(self, client: TestClient, auth_headers_admin: dict, db_session: Session):
        self._seed_logs(db_session)
        response = client.get("/api/v1/audit/logs?user_id_filter=2", headers=auth_headers_admin)
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert all(log["user_id"] == 2 for log in data["items"])

    def test_list_logs_ordered_by_timestamp_desc(
        self, client: TestClient, auth_headers_admin: dict, db_session: Session
    ):
        self._seed_logs(db_session)
        response = client.get("/api/v1/audit/logs?limit=6", headers=auth_headers_admin)
        assert response.status_code == 200
        items = response.json()["items"]
        # Most recent first (higher id = later timestamp due to seed order)
        ids = [item["id"] for item in items]
        assert ids == sorted(ids, reverse=True)


# ── Login audit trail integration ────────────────────────────────────────

class TestLoginAuditTrail:
    def test_failed_login_creates_audit_log(self, client: TestClient, db_session: Session):
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent", "password": "wrongpass123"},
        )
        assert response.status_code == 401

        audit_entry = db_session.query(AuditLog).filter(AuditLog.action == "login_failed").first()
        assert audit_entry is not None
        assert audit_entry.resource_type == "user"
        assert audit_entry.details["reason"] == "invalid_credentials"

    def test_successful_login_creates_audit_log(
        self, client: TestClient, db_session: Session, test_user_admin: User
    ):
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testadmin", "password": "adminpass123"},
        )
        assert response.status_code == 200

        audit_entry = db_session.query(AuditLog).filter(AuditLog.action == "login_success").first()
        assert audit_entry is not None
        assert audit_entry.resource_type == "user"
        assert audit_entry.details["username"] == "testadmin"
        assert audit_entry.details["role"] == "admin"
