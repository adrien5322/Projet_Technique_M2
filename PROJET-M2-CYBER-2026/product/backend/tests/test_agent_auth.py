"""Tests for agent authentication (X-Agent-Secret header).

Tests cover:
- verify_agent_secret dependency
- verify_agent_or_user combined dependency
- Agent auth on telemetry heartbeat endpoint
- Agent auth on events ingestion endpoint
- Rejection of invalid/missing agent secrets
"""

import pytest
from fastapi import status

from app.config import settings


class TestAgentSecretDependency:
    """Tests for verify_agent_secret dependency."""

    def test_valid_agent_secret_on_heartbeat(self, client, agent_secret_headers):
        """Test heartbeat endpoint with valid agent secret."""
        payload = {"status": "online", "cpu_usage": 45.0}

        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=agent_secret_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "online"

    def test_invalid_agent_secret_on_heartbeat(self, client):
        """Test heartbeat endpoint with invalid agent secret."""
        payload = {"status": "online"}
        headers = {"X-Agent-Secret": "wrong-secret-value"}

        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=headers,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_missing_agent_secret_on_heartbeat(self, client):
        """Test heartbeat endpoint without any authentication."""
        payload = {"status": "online"}

        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_valid_agent_secret_on_events(self, client, agent_secret_headers):
        """Test events ingestion endpoint with valid agent secret."""
        payload = {
            "event_type": "network_scan",
            "severity": "medium",
            "source_ip": "10.0.0.1",
        }

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=agent_secret_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["event_type"] == "network_scan"

    def test_invalid_agent_secret_on_events(self, client):
        """Test events endpoint with invalid agent secret."""
        payload = {"event_type": "other", "severity": "low"}
        headers = {"X-Agent-Secret": "invalid-secret"}

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=headers,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDualAuth:
    """Tests for dual authentication (JWT OR agent secret)."""

    def test_heartbeat_with_jwt_auth(self, client, auth_headers_analyst):
        """Test heartbeat still works with JWT auth."""
        payload = {"status": "online"}

        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_heartbeat_with_agent_auth(self, client, agent_secret_headers):
        """Test heartbeat works with agent secret auth."""
        payload = {"status": "warning", "cpu_usage": 80.0}

        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=agent_secret_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "warning"
        assert data["cpu_usage"] == 80.0

    def test_events_with_jwt_auth(self, client, auth_headers_admin):
        """Test events ingestion still works with JWT auth."""
        payload = {"event_type": "malware", "severity": "critical"}

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=auth_headers_admin,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_events_with_agent_auth(self, client, agent_secret_headers):
        """Test events ingestion works with agent secret auth."""
        payload = {"event_type": "data_exfiltration", "severity": "high"}

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=agent_secret_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_no_auth_rejected_on_heartbeat(self, client):
        """Test heartbeat rejects requests with no auth."""
        payload = {"status": "online"}

        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_no_auth_rejected_on_events(self, client):
        """Test events rejects requests with no auth."""
        payload = {"event_type": "other", "severity": "low"}

        response = client.post("/api/v1/events", json=payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAgentAuthReadEndpoints:
    """Tests that read endpoints still require JWT auth only."""

    def test_get_events_requires_jwt(self, client, agent_secret_headers):
        """Test GET /api/v1/events requires JWT, not agent secret."""
        response = client.get("/api/v1/events", headers=agent_secret_headers)

        # Agent secret should not be sufficient for read endpoints
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_event_by_id_requires_jwt(self, client, agent_secret_headers):
        """Test GET /api/v1/events/{id} requires JWT, not agent secret."""
        response = client.get("/api/v1/events/1", headers=agent_secret_headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_telemetry_requires_jwt(self, client, agent_secret_headers):
        """Test GET /api/v1/telemetry/{asset_id} requires JWT, not agent secret."""
        response = client.get("/api/v1/telemetry/1", headers=agent_secret_headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_telemetry_status_requires_jwt(self, client, agent_secret_headers):
        """Test GET /api/v1/telemetry/status requires JWT, not agent secret."""
        response = client.get("/api/v1/telemetry/status", headers=agent_secret_headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAgentSecretConfig:
    """Tests for AGENT_SECRET configuration."""

    def test_agent_secret_is_configured(self):
        """Test that AGENT_SECRET is set in settings."""
        assert settings.AGENT_SECRET is not None
        assert settings.AGENT_SECRET != ""
        assert settings.AGENT_SECRET == "test-agent-secret-change-me"

    def test_agent_secret_not_default_in_example(self):
        """Test that .env.example does not contain a real secret."""
        import pathlib
        env_example = pathlib.Path(__file__).parent.parent / ".env.example"
        if env_example.exists():
            content = env_example.read_text()
            assert "GENERATE_WITH_OPENSSL" in content
            # Should not contain a real hex secret
            assert "test-agent-secret" not in content
