"""Tests for the reports/export module.

Covers:
- Service functions (get_export_data, generate_csv, generate_json)
- Route access control (RBAC)
- CSV and JSON export format
- Summary endpoint
- Graceful handling of missing tables
- Date filtering for exports
"""

import csv
import io
import json
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from app.models.asset import Asset
from app.models.alert import Alert
from app.models.event import Event
from app.models.audit import AuditLog
from app.reports.service import generate_csv, generate_json, get_export_data


# ---------------------------------------------------------------------------
# Service unit tests
# ---------------------------------------------------------------------------

class TestGenerateCsv:
    """Unit tests for CSV generation."""

    def test_generate_csv_with_data(self):
        data = [
            {"hostname": "srv01", "ip_address": "10.0.0.1", "status": "active"},
            {"hostname": "srv02", "ip_address": "10.0.0.2", "status": "inactive"},
        ]
        content, filename = generate_csv(data, "assets")

        assert "assets_" in filename
        assert filename.endswith(".csv")

        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["hostname"] == "srv01"
        assert rows[1]["status"] == "inactive"

    def test_generate_csv_empty_data(self):
        content, filename = generate_csv([], "alerts")

        assert "alerts_" in filename
        assert "No data available" in content

    def test_generate_csv_filename_has_timestamp(self):
        _, filename = generate_csv([{"a": 1}], "events")
        # Format: events_YYYYMMDD_HHMMSS.csv
        parts = filename.replace(".csv", "").split("_")
        assert len(parts) >= 3  # events + date + time


class TestGenerateJson:
    """Unit tests for JSON generation."""

    def test_generate_json_with_data(self):
        data = [{"id": 1, "name": "test"}]
        content, filename = generate_json(data, "alerts")

        assert "alerts_" in filename
        assert filename.endswith(".json")

        payload = json.loads(content)
        assert "export_metadata" in payload
        assert "data" in payload
        assert payload["export_metadata"]["record_count"] == 1
        assert payload["export_metadata"]["source"] == "DAR-Cyber"
        assert len(payload["data"]) == 1

    def test_generate_json_empty_data(self):
        content, filename = generate_json([], "events")

        payload = json.loads(content)
        assert payload["export_metadata"]["record_count"] == 0
        assert payload["data"] == []

    def test_generate_json_metadata_has_timestamp(self):
        content, _ = generate_json([{"x": 1}], "audit")
        payload = json.loads(content)
        assert "generated_at" in payload["export_metadata"]


class TestGetExportData:
    """Unit tests for data retrieval."""

    def test_unknown_export_type_returns_empty(self, db_session):
        result = get_export_data(db_session, "nonexistent")
        assert result == []

    def test_assets_export_with_data(self, db_session):
        asset = Asset(
            hostname="test-srv",
            ip_address="192.168.1.10",
            asset_type="server",
            status="active",
        )
        db_session.add(asset)
        db_session.commit()

        result = get_export_data(db_session, "assets")
        assert len(result) == 1
        assert result[0]["hostname"] == "test-srv"

    def test_alerts_export_empty_table(self, db_session):
        # Alert table does not exist yet — should return empty list gracefully
        result = get_export_data(db_session, "alerts")
        assert result == []

    def test_events_export_empty_table(self, db_session):
        result = get_export_data(db_session, "events")
        assert result == []

    def test_audit_export_empty_table(self, db_session):
        result = get_export_data(db_session, "audit")
        assert result == []

    def test_date_filtering_alerts(self, db_session):
        """Test that date filtering works for alerts."""
        # Create alerts with different dates (use naive datetimes for SQLite compatibility)
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        two_days_ago = now - timedelta(days=2)

        alert1 = Alert(
            title="Old Alert",
            description="Created two days ago",
            severity="low",
            status="new",
            created_at=two_days_ago,
        )
        alert2 = Alert(
            title="Recent Alert",
            description="Created yesterday",
            severity="high",
            status="new",
            created_at=yesterday,
        )
        db_session.add_all([alert1, alert2])
        db_session.commit()

        # Filter from yesterday to now - should only return alert2
        from_date = yesterday.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "alerts", from_date=from_date)
        assert len(result) == 1
        assert result[0]["title"] == "Recent Alert"

        # Filter from two days ago to yesterday - should return both
        from_date = two_days_ago.strftime("%Y-%m-%d")
        to_date = yesterday.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "alerts", from_date=from_date, to_date=to_date)
        assert len(result) == 2

    def test_date_filtering_events(self, db_session):
        """Test that date filtering works for events."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        event1 = Event(
            event_type="login",
            severity="info",
            timestamp=yesterday,
        )
        event2 = Event(
            event_type="logout",
            severity="info",
            timestamp=now,
        )
        db_session.add_all([event1, event2])
        db_session.commit()

        # Filter from yesterday - should return both
        from_date = yesterday.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "events", from_date=from_date)
        assert len(result) == 2

        # Filter only today - should return only event2
        from_date = now.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "events", from_date=from_date)
        assert len(result) == 1
        assert result[0]["event_type"] == "logout"

    def test_date_filtering_audit_logs(self, db_session):
        """Test that date filtering works for audit logs."""
        now = datetime.now()
        last_week = now - timedelta(days=7)

        audit1 = AuditLog(
            action="create",
            resource_type="asset",
            timestamp=last_week,
        )
        audit2 = AuditLog(
            action="update",
            resource_type="alert",
            timestamp=now,
        )
        db_session.add_all([audit1, audit2])
        db_session.commit()

        # Filter from last week to now - should return both
        from_date = last_week.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "audit", from_date=from_date)
        assert len(result) == 2

        # Filter only today - should return only audit2
        from_date = now.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "audit", from_date=from_date)
        assert len(result) == 1
        assert result[0]["action"] == "update"

    def test_date_filtering_assets(self, db_session):
        """Test that date filtering works for assets."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        asset1 = Asset(
            hostname="old-srv",
            asset_type="server",
            status="active",
            created_at=yesterday,
        )
        asset2 = Asset(
            hostname="new-srv",
            asset_type="workstation",
            status="active",
            created_at=now,
        )
        db_session.add_all([asset1, asset2])
        db_session.commit()

        # Filter from yesterday - should return both
        from_date = yesterday.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "assets", from_date=from_date)
        assert len(result) == 2

        # Filter only today - should return only asset2
        from_date = now.strftime("%Y-%m-%d")
        result = get_export_data(db_session, "assets", from_date=from_date)
        assert len(result) == 1
        assert result[0]["hostname"] == "new-srv"

    def test_invalid_date_format_ignored(self, db_session):
        """Test that invalid date formats are ignored gracefully."""
        asset = Asset(
            hostname="test-srv",
            asset_type="server",
            status="active",
        )
        db_session.add(asset)
        db_session.commit()

        # Invalid date should not filter anything
        result = get_export_data(db_session, "assets", from_date="invalid-date")
        assert len(result) == 1


# ---------------------------------------------------------------------------
# Route integration tests
# ---------------------------------------------------------------------------

class TestExportAlertsCsv:
    """Tests for GET /api/v1/export/alerts/csv."""

    def test_requires_auth(self, client):
        response = client.get("/api/v1/export/alerts/csv")
        assert response.status_code in (401, 403)

    def test_analyst_can_access(self, client, auth_headers_analyst):
        response = client.get(
            "/api/v1/export/alerts/csv", headers=auth_headers_analyst
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"

    def test_admin_can_access(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/alerts/csv", headers=auth_headers_admin
        )
        assert response.status_code == 200

    def test_returns_csv_content(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/alerts/csv", headers=auth_headers_admin
        )
        assert "attachment" in response.headers.get("content-disposition", "")
        assert "alerts_" in response.headers.get("content-disposition", "")


class TestExportAlertsJson:
    """Tests for GET /api/v1/export/alerts/json."""

    def test_analyst_can_access(self, client, auth_headers_analyst):
        response = client.get(
            "/api/v1/export/alerts/json", headers=auth_headers_analyst
        )
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_returns_valid_json(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/alerts/json", headers=auth_headers_admin
        )
        payload = json.loads(response.content)
        assert "export_metadata" in payload
        assert "data" in payload


class TestExportEventsCsv:
    """Tests for GET /api/v1/export/events/csv."""

    def test_analyst_can_access(self, client, auth_headers_analyst):
        response = client.get(
            "/api/v1/export/events/csv", headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_admin_can_access(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/events/csv", headers=auth_headers_admin
        )
        assert response.status_code == 200


class TestExportEventsJson:
    """Tests for GET /api/v1/export/events/json."""

    def test_analyst_can_access(self, client, auth_headers_analyst):
        response = client.get(
            "/api/v1/export/events/json", headers=auth_headers_analyst
        )
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_admin_can_access(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/events/json", headers=auth_headers_admin
        )
        assert response.status_code == 200

    def test_returns_valid_json(self, client, auth_headers_admin):
        """Export should return a valid JSON structure with metadata."""
        response = client.get(
            "/api/v1/export/events/json", headers=auth_headers_admin
        )
        assert response.status_code == 200

        payload = json.loads(response.content)
        assert "export_metadata" in payload
        assert "data" in payload
        assert payload["export_metadata"]["source"] == "DAR-Cyber"
        assert "record_count" in payload["export_metadata"]

    def test_returns_json_attachment(self, client, auth_headers_admin):
        """Response should have attachment disposition with .json filename."""
        response = client.get(
            "/api/v1/export/events/json", headers=auth_headers_admin
        )
        assert response.status_code == 200

        content_disp = response.headers.get("content-disposition", "")
        assert "attachment" in content_disp
        assert "events_" in content_disp
        assert ".json" in content_disp

    def test_unauthenticated_forbidden(self, client):
        """Unauthenticated users should not access events JSON export."""
        response = client.get("/api/v1/export/events/json")
        assert response.status_code in (401, 403)


class TestExportAuditCsv:
    """Tests for GET /api/v1/export/audit/csv (admin only)."""

    def test_analyst_forbidden(self, client, auth_headers_analyst):
        response = client.get(
            "/api/v1/export/audit/csv", headers=auth_headers_analyst
        )
        assert response.status_code == 403

    def test_admin_can_access(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/audit/csv", headers=auth_headers_admin
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"

    def test_unauthenticated_forbidden(self, client):
        response = client.get("/api/v1/export/audit/csv")
        assert response.status_code in (401, 403)


class TestExportAuditJson:
    """Tests for GET /api/v1/export/audit/json (admin only)."""

    def test_analyst_forbidden(self, client, auth_headers_analyst):
        """Analyst should not be able to export audit logs as JSON."""
        response = client.get(
            "/api/v1/export/audit/json", headers=auth_headers_analyst
        )
        assert response.status_code == 403

    def test_admin_can_access(self, client, auth_headers_admin):
        """Admin should be able to export audit logs as JSON."""
        response = client.get(
            "/api/v1/export/audit/json", headers=auth_headers_admin
        )
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    def test_returns_valid_json(self, client, auth_headers_admin):
        """Export should return a valid JSON structure with metadata."""
        response = client.get(
            "/api/v1/export/audit/json", headers=auth_headers_admin
        )
        assert response.status_code == 200

        payload = json.loads(response.content)
        assert "export_metadata" in payload
        assert "data" in payload
        assert payload["export_metadata"]["source"] == "DAR-Cyber"
        assert "record_count" in payload["export_metadata"]

    def test_unauthenticated_forbidden(self, client):
        """Unauthenticated users should not access audit JSON export."""
        response = client.get("/api/v1/export/audit/json")
        assert response.status_code in (401, 403)

    def test_returns_json_attachment(self, client, auth_headers_admin):
        """Response should have attachment disposition with .json filename."""
        response = client.get(
            "/api/v1/export/audit/json", headers=auth_headers_admin
        )
        assert response.status_code == 200

        content_disp = response.headers.get("content-disposition", "")
        assert "attachment" in content_disp
        assert "audit_" in content_disp
        assert ".json" in content_disp


class TestExportWithDateFiltering:
    """Tests for date filtering on export endpoints."""

    def test_alerts_csv_with_date_filter(self, client, auth_headers_admin, db_session):
        """Test that alerts CSV export supports date filtering."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        # Create test alerts
        alert1 = Alert(
            title="Old Alert",
            description="Old",
            severity="low",
            status="new",
            created_at=yesterday,
        )
        alert2 = Alert(
            title="New Alert",
            description="New",
            severity="high",
            status="new",
            created_at=now,
        )
        db_session.add_all([alert1, alert2])
        db_session.commit()

        # Filter from today - should return only alert2
        from_date = now.strftime("%Y-%m-%d")
        response = client.get(
            f"/api/v1/export/alerts/csv?from_date={from_date}",
            headers=auth_headers_admin,
        )
        assert response.status_code == 200

        reader = csv.DictReader(io.StringIO(response.text))
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["title"] == "New Alert"

    def test_alerts_json_with_date_filter(self, client, auth_headers_admin, db_session):
        """Test that alerts JSON export supports date filtering."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        # Create test alerts
        alert1 = Alert(
            title="Old Alert",
            description="Old",
            severity="low",
            status="new",
            created_at=yesterday,
        )
        alert2 = Alert(
            title="New Alert",
            description="New",
            severity="high",
            status="new",
            created_at=now,
        )
        db_session.add_all([alert1, alert2])
        db_session.commit()

        # Filter from today - should return only alert2
        from_date = now.strftime("%Y-%m-%d")
        response = client.get(
            f"/api/v1/export/alerts/json?from_date={from_date}",
            headers=auth_headers_admin,
        )
        assert response.status_code == 200

        payload = json.loads(response.content)
        assert payload["export_metadata"]["record_count"] == 1
        assert payload["data"][0]["title"] == "New Alert"

    def test_events_csv_with_date_filter(self, client, auth_headers_analyst, db_session):
        """Test that events CSV export supports date filtering."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        # Create test events
        event1 = Event(
            event_type="login",
            severity="info",
            timestamp=yesterday,
        )
        event2 = Event(
            event_type="logout",
            severity="info",
            timestamp=now,
        )
        db_session.add_all([event1, event2])
        db_session.commit()

        # Filter from today - should return only event2
        from_date = now.strftime("%Y-%m-%d")
        response = client.get(
            f"/api/v1/export/events/csv?from_date={from_date}",
            headers=auth_headers_analyst,
        )
        assert response.status_code == 200

        reader = csv.DictReader(io.StringIO(response.text))
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["event_type"] == "logout"

    def test_audit_csv_with_date_filter(self, client, auth_headers_admin, db_session):
        """Test that audit CSV export supports date filtering (admin only)."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        # Create test audit logs
        audit1 = AuditLog(
            action="create",
            resource_type="asset",
            timestamp=yesterday,
        )
        audit2 = AuditLog(
            action="delete",
            resource_type="alert",
            timestamp=now,
        )
        db_session.add_all([audit1, audit2])
        db_session.commit()

        # Filter from today - should return only audit2
        from_date = now.strftime("%Y-%m-%d")
        response = client.get(
            f"/api/v1/export/audit/csv?from_date={from_date}",
            headers=auth_headers_admin,
        )
        assert response.status_code == 200

        reader = csv.DictReader(io.StringIO(response.text))
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["action"] == "delete"

    def test_summary_with_date_filter(self, client, auth_headers_admin, db_session):
        """Test that summary endpoint supports date filtering."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        # Create test assets
        asset1 = Asset(
            hostname="old-srv",
            asset_type="server",
            status="active",
            created_at=yesterday,
        )
        asset2 = Asset(
            hostname="new-srv",
            asset_type="workstation",
            status="active",
            created_at=now,
        )
        db_session.add_all([asset1, asset2])
        db_session.commit()

        # Filter from today - should count only asset2
        from_date = now.strftime("%Y-%m-%d")
        response = client.get(
            f"/api/v1/export/summary?from_date={from_date}",
            headers=auth_headers_admin,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["summary"]["assets"]["count"] == 1

    def test_date_filter_with_to_date(self, client, auth_headers_admin, db_session):
        """Test date filtering with both from_date and to_date."""
        now = datetime.now()
        two_days_ago = now - timedelta(days=2)
        yesterday = now - timedelta(days=1)

        # Create test alerts
        alert1 = Alert(
            title="Old Alert",
            description="Old",
            severity="low",
            status="new",
            created_at=two_days_ago,
        )
        alert2 = Alert(
            title="Middle Alert",
            description="Middle",
            severity="medium",
            status="new",
            created_at=yesterday,
        )
        alert3 = Alert(
            title="New Alert",
            description="New",
            severity="high",
            status="new",
            created_at=now,
        )
        db_session.add_all([alert1, alert2, alert3])
        db_session.commit()

        # Filter from two days ago to yesterday - should return alert1 and alert2
        from_date = two_days_ago.strftime("%Y-%m-%d")
        to_date = yesterday.strftime("%Y-%m-%d")
        response = client.get(
            f"/api/v1/export/alerts/json?from_date={from_date}&to_date={to_date}",
            headers=auth_headers_admin,
        )
        assert response.status_code == 200

        payload = json.loads(response.content)
        assert payload["export_metadata"]["record_count"] == 2

    def test_invalid_date_format_returns_all(self, client, auth_headers_admin, db_session):
        """Test that invalid date format returns all records."""
        # Create test alerts
        alert = Alert(
            title="Test Alert",
            description="Test",
            severity="low",
            status="new",
        )
        db_session.add(alert)
        db_session.commit()

        # Invalid date should not filter
        response = client.get(
            "/api/v1/export/alerts/json?from_date=invalid-date",
            headers=auth_headers_admin,
        )
        assert response.status_code == 200

        payload = json.loads(response.content)
        assert payload["export_metadata"]["record_count"] == 1


class TestExportAssetsCsv:
    """Tests for GET /api/v1/export/assets/csv."""

    def test_analyst_can_access(self, client, auth_headers_analyst):
        response = client.get(
            "/api/v1/export/assets/csv", headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_returns_asset_data(self, client, auth_headers_admin, db_session):
        asset = Asset(
            hostname="export-test-srv",
            ip_address="10.10.10.10",
            asset_type="workstation",
            status="active",
        )
        db_session.add(asset)
        db_session.commit()

        response = client.get(
            "/api/v1/export/assets/csv", headers=auth_headers_admin
        )
        assert response.status_code == 200

        reader = csv.DictReader(io.StringIO(response.text))
        rows = list(reader)
        hostnames = [r["hostname"] for r in rows]
        assert "export-test-srv" in hostnames


class TestExportSummary:
    """Tests for GET /api/v1/export/summary."""

    def test_analyst_can_access(self, client, auth_headers_analyst):
        response = client.get(
            "/api/v1/export/summary", headers=auth_headers_analyst
        )
        assert response.status_code == 200

    def test_admin_can_access(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/summary", headers=auth_headers_admin
        )
        assert response.status_code == 200

    def test_summary_structure(self, client, auth_headers_admin):
        response = client.get(
            "/api/v1/export/summary", headers=auth_headers_admin
        )
        data = response.json()
        assert "summary" in data
        assert "generated_by" in data

        summary = data["summary"]
        for entity in ["alerts", "events", "audit", "assets"]:
            assert entity in summary
            assert "count" in summary[entity]
            assert "exportable" in summary[entity]

    def test_summary_includes_asset_count(self, client, auth_headers_admin, db_session):
        for i in range(3):
            db_session.add(Asset(
                hostname=f"summary-srv-{i}",
                asset_type="server",
                status="active",
            ))
        db_session.commit()

        response = client.get(
            "/api/v1/export/summary", headers=auth_headers_admin
        )
        data = response.json()
        assert data["summary"]["assets"]["count"] >= 3
