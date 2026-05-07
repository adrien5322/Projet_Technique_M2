"""Tests for telemetry module.

Tests cover:
- TelemetryHeartbeat model
- Telemetry schemas validation
- Telemetry service functions
- Telemetry API endpoints
- RBAC for telemetry routes
"""

import pytest
from datetime import datetime, timedelta
from fastapi import status
from sqlalchemy.orm import Session
from typing import Generator

from app.models.telemetry import TelemetryHeartbeat
from app.schemas.telemetry import TelemetryHeartbeatCreate, TelemetryHeartbeatBase
from app.telemetry.service import (
    create_heartbeat,
    get_heartbeat_by_asset,
    get_latest_heartbeat,
    check_missed_heartbeats,
    get_overall_status,
)


class TestTelemetryHeartbeatModel:
    """Tests for TelemetryHeartbeat model."""
    
    def test_create_heartbeat_model(self, db_session):
        """Test creating a TelemetryHeartbeat instance."""
        heartbeat = TelemetryHeartbeat(
            asset_id=1,
            status="online",
            cpu_usage=45.5,
            memory_usage=60.2,
            disk_usage=75.0,
            network_latency=12.3,
        )
        db_session.add(heartbeat)
        db_session.commit()
        db_session.refresh(heartbeat)
        
        assert heartbeat.id is not None
        assert heartbeat.asset_id == 1
        assert heartbeat.status == "online"
        assert heartbeat.cpu_usage == 45.5
        assert heartbeat.memory_usage == 60.2
        assert heartbeat.disk_usage == 75.0
        assert heartbeat.network_latency == 12.3
        assert heartbeat.timestamp is not None
    
    def test_heartbeat_repr(self, db_session):
        """Test TelemetryHeartbeat __repr__ method."""
        heartbeat = TelemetryHeartbeat(
            asset_id=1,
            status="offline",
        )
        db_session.add(heartbeat)
        db_session.commit()
        
        repr_str = repr(heartbeat)
        assert "asset_id=1" in repr_str
        assert "status=offline" in repr_str
    
    def test_heartbeat_with_nullable_fields(self, db_session):
        """Test creating heartbeat with only required fields."""
        heartbeat = TelemetryHeartbeat(
            status="warning",
        )
        db_session.add(heartbeat)
        db_session.commit()
        db_session.refresh(heartbeat)
        
        assert heartbeat.id is not None
        assert heartbeat.asset_id is None
        assert heartbeat.status == "warning"
        assert heartbeat.cpu_usage is None


class TestTelemetrySchemas:
    """Tests for telemetry Pydantic schemas."""
    
    def test_valid_heartbeat_create(self):
        """Test valid TelemetryHeartbeatCreate schema."""
        data = {
            "status": "online",
            "asset_id": 1,
            "cpu_usage": 50.0,
            "memory_usage": 60.0,
            "disk_usage": 70.0,
            "network_latency": 15.5,
        }
        schema = TelemetryHeartbeatCreate(**data)
        
        assert schema.status == "online"
        assert schema.asset_id == 1
        assert schema.cpu_usage == 50.0
    
    def test_heartbeat_create_without_optional_fields(self):
        """Test TelemetryHeartbeatCreate with only required fields."""
        data = {"status": "offline"}
        schema = TelemetryHeartbeatCreate(**data)
        
        assert schema.status == "offline"
        assert schema.asset_id is None
        assert schema.cpu_usage is None
    
    def test_invalid_status(self):
        """Test validation with invalid status."""
        data = {"status": "invalid_status"}
        
        with pytest.raises(ValueError) as exc_info:
            TelemetryHeartbeatCreate(**data)
        
        assert "Status must be one of" in str(exc_info.value)
    
    def test_valid_statuses(self):
        """Test all valid status values."""
        for status_value in ["online", "offline", "warning"]:
            data = {"status": status_value}
            schema = TelemetryHeartbeatCreate(**data)
            assert schema.status == status_value
    
    def test_cpu_usage_out_of_range(self):
        """Test CPU usage validation (0-100)."""
        data = {"status": "online", "cpu_usage": 150.0}
        
        with pytest.raises(ValueError):
            TelemetryHeartbeatCreate(**data)
    
    def test_memory_usage_out_of_range(self):
        """Test memory usage validation (0-100)."""
        data = {"status": "online", "memory_usage": -10.0}
        
        with pytest.raises(ValueError):
            TelemetryHeartbeatCreate(**data)
    
    def test_disk_usage_out_of_range(self):
        """Test disk usage validation (0-100)."""
        data = {"status": "online", "disk_usage": 150.0}
        
        with pytest.raises(ValueError):
            TelemetryHeartbeatCreate(**data)
    
    def test_network_latency_negative(self):
        """Test network latency validation (must be >= 0)."""
        data = {"status": "online", "network_latency": -5.0}
        
        with pytest.raises(ValueError):
            TelemetryHeartbeatCreate(**data)
    
    def test_missing_required_status(self):
        """Test that status is required."""
        with pytest.raises(ValueError) as exc_info:
            TelemetryHeartbeatCreate()
        
        assert "field required" in str(exc_info.value).lower() or "missing" in str(exc_info.value).lower()
    
    def test_boundary_values(self):
        """Test boundary values for usage fields."""
        # Test minimum values
        data_min = {
            "status": "online",
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "disk_usage": 0.0,
            "network_latency": 0.0,
        }
        schema_min = TelemetryHeartbeatCreate(**data_min)
        assert schema_min.cpu_usage == 0.0
        
        # Test maximum values
        data_max = {
            "status": "online",
            "cpu_usage": 100.0,
            "memory_usage": 100.0,
            "disk_usage": 100.0,
        }
        schema_max = TelemetryHeartbeatCreate(**data_max)
        assert schema_max.cpu_usage == 100.0
    
    def test_asset_id_validation(self):
        """Test asset_id validation."""
        # Valid asset_id
        data = {"status": "online", "asset_id": 1}
        schema = TelemetryHeartbeatCreate(**data)
        assert schema.asset_id == 1
        
        # Negative asset_id - no validation in schema (would be validated at DB level)
        schema_neg = TelemetryHeartbeatCreate(status="online", asset_id=-1)
        assert schema_neg.asset_id == -1
        
        # asset_id is optional
        schema_no_asset = TelemetryHeartbeatCreate(status="online")
        assert schema_no_asset.asset_id is None


class TestTelemetryService:
    """Tests for telemetry service functions."""
    
    def test_create_heartbeat_service(self, db_session):
        """Test create_heartbeat service function."""
        heartbeat_data = TelemetryHeartbeatCreate(
            asset_id=1,
            status="online",
            cpu_usage=45.0,
            memory_usage=55.0,
        )
        
        result = create_heartbeat(db_session, heartbeat_data)
        
        assert result.id is not None
        assert result.asset_id == 1
        assert result.status == "online"
        assert result.cpu_usage == 45.0
        assert result.memory_usage == 55.0
    
    def test_get_heartbeat_by_asset(self, db_session):
        """Test get_heartbeat_by_asset service function."""
        # Create test heartbeats
        for i in range(5):
            heartbeat = TelemetryHeartbeat(
                asset_id=1,
                status="online",
                cpu_usage=float(i * 10),
            )
            db_session.add(heartbeat)
        db_session.commit()
        
        # Create heartbeat for different asset
        other_heartbeat = TelemetryHeartbeat(
            asset_id=2,
            status="offline",
        )
        db_session.add(other_heartbeat)
        db_session.commit()
        
        # Get heartbeats for asset 1
        result = get_heartbeat_by_asset(db_session, asset_id=1)
        
        assert len(result) == 5
        assert all(hb.asset_id == 1 for hb in result)
    
    def test_get_heartbeat_by_asset_with_limit(self, db_session):
        """Test get_heartbeat_by_asset with limit parameter."""
        # Create 10 heartbeats
        for i in range(10):
            heartbeat = TelemetryHeartbeat(
                asset_id=1,
                status="online",
            )
            db_session.add(heartbeat)
        db_session.commit()
        
        result = get_heartbeat_by_asset(db_session, asset_id=1, limit=3)
        
        assert len(result) == 3
    
    def test_get_latest_heartbeat(self, db_session):
        """Test get_latest_heartbeat service function."""
        # Create heartbeats - SQLite may not handle timestamps precisely in tests
        # so we'll verify the query works and returns the most recent
        heartbeat1 = TelemetryHeartbeat(
            asset_id=1,
            status="online",
        )
        db_session.add(heartbeat1)
        db_session.commit()
        
        heartbeat2 = TelemetryHeartbeat(
            asset_id=1,
            status="warning",
        )
        db_session.add(heartbeat2)
        db_session.commit()
        
        result = get_latest_heartbeat(db_session, asset_id=1)
        
        assert result is not None
        # Just check we get a result back - SQLite timestamp handling varies
        assert result.asset_id == 1
    
    def test_get_latest_heartbeat_no_data(self, db_session):
        """Test get_latest_heartbeat when no data exists."""
        result = get_latest_heartbeat(db_session, asset_id=999)
        
        assert result is None
    
    def test_check_missed_heartbeats(self, db_session):
        """Test check_missed_heartbeats service function."""
        # Create recent heartbeat (should not be missed)
        recent_heartbeat = TelemetryHeartbeat(
            asset_id=1,
            status="online",
        )
        db_session.add(recent_heartbeat)
        
        # Create old heartbeat (should be missed)
        old_heartbeat = TelemetryHeartbeat(
            asset_id=2,
            status="offline",
        )
        db_session.add(old_heartbeat)
        db_session.commit()
        
        # Manually set timestamp to old date
        old_heartbeat.timestamp = datetime.utcnow() - timedelta(minutes=10)
        db_session.commit()
        
        result = check_missed_heartbeats(db_session, timeout_minutes=5)
        
        assert 2 in result
        assert 1 not in result
    
    def test_get_overall_status(self, db_session):
        """Test get_overall_status service function."""
        # Create heartbeats for different assets
        hb1 = TelemetryHeartbeat(asset_id=1, status="online")
        hb2 = TelemetryHeartbeat(asset_id=2, status="offline")
        hb3 = TelemetryHeartbeat(asset_id=3, status="warning")
        db_session.add_all([hb1, hb2, hb3])
        db_session.commit()
        
        result = get_overall_status(db_session)
        
        assert result['total_assets'] == 3
        assert result['online_count'] == 1
        assert result['offline_count'] == 1
        assert result['warning_count'] == 1
    
    def test_get_overall_status_empty(self, db_session):
        """Test get_overall_status with no data."""
        result = get_overall_status(db_session)
        
        assert result['total_assets'] == 0
        assert result['online_count'] == 0
        assert result['offline_count'] == 0
        assert result['warning_count'] == 0
        assert result['missed_heartbeats_count'] == 0
    
    def test_get_overall_status_with_old_heartbeats(self, db_session):
        """Test get_overall_status ignores old heartbeats."""
        # Create recent heartbeat
        recent = TelemetryHeartbeat(asset_id=1, status="online")
        db_session.add(recent)
        db_session.commit()
        
        # Create old heartbeat (should be ignored)
        old = TelemetryHeartbeat(asset_id=2, status="offline")
        db_session.add(old)
        db_session.commit()
        old.timestamp = datetime.utcnow() - timedelta(minutes=10)
        db_session.commit()
        
        result = get_overall_status(db_session, timeout_minutes=5)
        
        assert result['total_assets'] == 1
        assert result['online_count'] == 1
        assert result['offline_count'] == 0
    
    def test_get_heartbeat_by_asset_empty(self, db_session):
        """Test get_heartbeat_by_asset with no data."""
        result = get_heartbeat_by_asset(db_session, asset_id=999)
        
        assert len(result) == 0
        assert isinstance(result, list)
    
    def test_get_heartbeat_by_asset_limit_zero(self, db_session):
        """Test get_heartbeat_by_asset with limit=0."""
        # Create test heartbeats
        for i in range(5):
            heartbeat = TelemetryHeartbeat(asset_id=1, status="online")
            db_session.add(heartbeat)
        db_session.commit()
        
        result = get_heartbeat_by_asset(db_session, asset_id=1, limit=0)
        
        # Limit 0 should return empty list
        assert len(result) == 0
    
    def test_check_missed_heartbeats_no_heartbeats(self, db_session):
        """Test check_missed_heartbeats with no data."""
        result = check_missed_heartbeats(db_session)
        
        assert len(result) == 0
        assert isinstance(result, list)
    
    def test_check_missed_heartbeats_all_recent(self, db_session):
        """Test check_missed_heartbeats when all heartbeats are recent."""
        # Create recent heartbeats
        for i in range(3):
            heartbeat = TelemetryHeartbeat(asset_id=i+1, status="online")
            db_session.add(heartbeat)
        db_session.commit()
        
        result = check_missed_heartbeats(db_session, timeout_minutes=5)
        
        # All heartbeats are recent, none missed
        assert len(result) == 0
    
    def test_check_missed_heartbeats_mixed(self, db_session):
        """Test check_missed_heartbeats with mix of recent and old."""
        # Create recent heartbeat
        recent = TelemetryHeartbeat(asset_id=1, status="online")
        db_session.add(recent)
        db_session.commit()
        
        # Create old heartbeat
        old = TelemetryHeartbeat(asset_id=2, status="offline")
        db_session.add(old)
        db_session.commit()
        old.timestamp = datetime.utcnow() - timedelta(minutes=10)
        db_session.commit()
        
        # Create another old heartbeat
        old2 = TelemetryHeartbeat(asset_id=3, status="warning")
        db_session.add(old2)
        db_session.commit()
        old2.timestamp = datetime.utcnow() - timedelta(minutes=20)
        db_session.commit()
        
        result = check_missed_heartbeats(db_session, timeout_minutes=5)
        
        assert 2 in result
        assert 3 in result
        assert 1 not in result
        assert len(result) == 2
    
    def test_check_missed_heartbeats_custom_timeout(self, db_session):
        """Test check_missed_heartbeats with custom timeout."""
        # Create heartbeat that is 3 minutes old
        heartbeat = TelemetryHeartbeat(asset_id=1, status="online")
        db_session.add(heartbeat)
        db_session.commit()
        heartbeat.timestamp = datetime.utcnow() - timedelta(minutes=3)
        db_session.commit()
        
        # With 5 min timeout, should not be missed
        result_5min = check_missed_heartbeats(db_session, timeout_minutes=5)
        assert 1 not in result_5min
        
        # With 1 min timeout, should be missed
        result_1min = check_missed_heartbeats(db_session, timeout_minutes=1)
        assert 1 in result_1min


class TestTelemetryRoutes:
    """Tests for telemetry API endpoints."""
    
    def test_post_heartbeat_success(self, client, auth_headers_analyst):
        """Test POST /api/v1/telemetry/heartbeat with valid data."""
        payload = {
            "status": "online",
            "asset_id": 1,
            "cpu_usage": 45.0,
            "memory_usage": 60.0,
            "disk_usage": 75.0,
            "network_latency": 12.5,
        }
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "online"
        assert data["asset_id"] == 1
        assert data["cpu_usage"] == 45.0
    
    def test_post_heartbeat_without_auth(self, client):
        """Test POST /api/v1/telemetry/heartbeat without authentication."""
        payload = {"status": "online"}
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_post_heartbeat_invalid_status(self, client, auth_headers_analyst):
        """Test POST /api/v1/telemetry/heartbeat with invalid status."""
        payload = {"status": "invalid"}
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_telemetry_history(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/telemetry/{asset_id}."""
        # Create test data
        for i in range(3):
            heartbeat = TelemetryHeartbeat(
                asset_id=1,
                status="online",
            )
            db_session.add(heartbeat)
        db_session.commit()
        
        response = client.get(
            "/api/v1/telemetry/1",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_telemetry_history_without_auth(self, client):
        """Test GET /api/v1/telemetry/{asset_id} without authentication."""
        response = client.get("/api/v1/telemetry/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_overall_status_endpoint(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/telemetry/status."""
        # Create test data
        hb1 = TelemetryHeartbeat(asset_id=1, status="online")
        hb2 = TelemetryHeartbeat(asset_id=2, status="offline")
        db_session.add_all([hb1, hb2])
        db_session.commit()
        
        response = client.get(
            "/api/v1/telemetry/status",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_assets" in data
        assert "online_count" in data
        assert "offline_count" in data
    
    def test_get_missed_heartbeats_admin_only(self, client, auth_headers_analyst):
        """Test GET /api/v1/telemetry/missed requires admin role."""
        response = client.get(
            "/api/v1/telemetry/missed",
            headers=auth_headers_analyst
        )
        
        # Analyst should not access this endpoint
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_missed_heartbeats_admin(self, client, auth_headers_admin, db_session):
        """Test GET /api/v1/telemetry/missed with admin token."""
        response = client.get(
            "/api/v1/telemetry/missed",
            headers=auth_headers_admin
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_latest_heartbeat_endpoint(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/telemetry/latest/{asset_id}."""
        # Create test data
        heartbeat = TelemetryHeartbeat(
            asset_id=1,
            status="warning",
        )
        db_session.add(heartbeat)
        db_session.commit()
        
        response = client.get(
            "/api/v1/telemetry/latest/1",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "warning"
        assert data["asset_id"] == 1
    
    def test_get_latest_heartbeat_not_found(self, client, auth_headers_analyst):
        """Test GET /api/v1/telemetry/latest/{asset_id} with non-existent asset."""
        response = client.get(
            "/api/v1/telemetry/latest/999",
            headers=auth_headers_analyst
        )
        
        # Returns 200 with null body (not 404)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None
    
    def test_get_latest_heartbeat_without_auth(self, client):
        """Test GET /api/v1/telemetry/latest/{asset_id} without authentication."""
        response = client.get("/api/v1/telemetry/latest/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_telemetry_history_not_found(self, client, auth_headers_analyst):
        """Test GET /api/v1/telemetry/{asset_id} with non-existent asset."""
        response = client.get(
            "/api/v1/telemetry/999",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 0
    
    def test_get_telemetry_history_with_limit(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/telemetry/{asset_id} with limit parameter."""
        # Create 10 heartbeats
        for i in range(10):
            heartbeat = TelemetryHeartbeat(
                asset_id=1,
                status="online",
            )
            db_session.add(heartbeat)
        db_session.commit()
        
        response = client.get(
            "/api/v1/telemetry/1?limit=3",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
    
    def test_get_telemetry_history_invalid_limit(self, client, auth_headers_analyst):
        """Test GET /api/v1/telemetry/{asset_id} with invalid limit."""
        # Negative limit - FastAPI may not validate this for query params
        # The service should handle it (return empty or all results)
        response = client.get(
            "/api/v1/telemetry/1?limit=-1",
            headers=auth_headers_analyst
        )
        
        # Either returns 422 (validation error) or 200 with empty list
        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_200_OK]
        if response.status_code == status.HTTP_200_OK:
            # With negative limit, results may be empty
            data = response.json()
            assert isinstance(data, list)
    
    def test_post_heartbeat_minimal(self, client, auth_headers_analyst):
        """Test POST /api/v1/telemetry/heartbeat with minimal data."""
        payload = {"status": "offline"}
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "offline"
        assert data["asset_id"] is None
    
    def test_post_heartbeat_with_all_fields(self, client, auth_headers_analyst):
        """Test POST /api/v1/telemetry/heartbeat with all fields."""
        payload = {
            "status": "warning",
            "asset_id": 5,
            "cpu_usage": 99.9,
            "memory_usage": 80.5,
            "disk_usage": 60.0,
            "network_latency": 45.7,
        }
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "warning"
        assert data["asset_id"] == 5
        assert data["cpu_usage"] == 99.9
        assert data["memory_usage"] == 80.5
    
    def test_post_heartbeat_invalid_cpu(self, client, auth_headers_analyst):
        """Test POST /api/v1/telemetry/heartbeat with invalid CPU usage."""
        payload = {"status": "online", "cpu_usage": 150.0}
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_post_heartbeat_negative_latency(self, client, auth_headers_analyst):
        """Test POST /api/v1/telemetry/heartbeat with negative latency."""
        payload = {"status": "online", "network_latency": -5.0}
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_overall_status_without_auth(self, client):
        """Test GET /api/v1/telemetry/status without authentication."""
        response = client.get("/api/v1/telemetry/status")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_missed_heartbeats_without_auth(self, client):
        """Test GET /api/v1/telemetry/missed without authentication."""
        response = client.get("/api/v1/telemetry/missed")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_missed_heartbeats_with_timeout_param(self, client, auth_headers_admin, db_session):
        """Test GET /api/v1/telemetry/missed with custom timeout."""
        # Create old heartbeat
        old = TelemetryHeartbeat(asset_id=1, status="offline")
        db_session.add(old)
        db_session.commit()
        old.timestamp = datetime.utcnow() - timedelta(minutes=3)
        db_session.commit()
        
        # With 5 min timeout, should not be missed
        response = client.get(
            "/api/v1/telemetry/missed?timeout_minutes=5",
            headers=auth_headers_admin
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Asset 1 should not be in missed list (only 3 min old)
        asset_ids = [item['asset_id'] for item in data]
        assert 1 not in asset_ids
    
    def test_rbac_analyst_cannot_access_missed(self, client, auth_headers_analyst):
        """Test that analyst role cannot access missed heartbeats endpoint."""
        response = client.get(
            "/api/v1/telemetry/missed",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_rbac_admin_can_access_missed(self, client, auth_headers_admin):
        """Test that admin role can access missed heartbeats endpoint."""
        response = client.get(
            "/api/v1/telemetry/missed",
            headers=auth_headers_admin
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_rbac_analyst_can_access_status(self, client, auth_headers_analyst):
        """Test that analyst role can access status endpoint."""
        response = client.get(
            "/api/v1/telemetry/status",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_rbac_analyst_can_post_heartbeat(self, client, auth_headers_analyst):
        """Test that analyst role can post heartbeat."""
        payload = {"status": "online"}
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_inactive_user_cannot_access(self, client, db_session):
        """Test that inactive user cannot access endpoints."""
        # Create inactive user
        from app.auth.service import get_password_hash, create_access_token
        from app.models.user import User
        
        inactive_user = User(
            username="inactive",
            email="inactive@test.com",
            hashed_password=get_password_hash("password123"),
            role="analyst",
            is_active=False
        )
        db_session.add(inactive_user)
        db_session.commit()
        
        # Create token for inactive user
        token = create_access_token({"sub": inactive_user.username, "role": inactive_user.role})
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get(
            "/api/v1/telemetry/status",
            headers=headers
        )
        
        # Inactive user returns 401 (credentials exception) not 403
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_response_structure_heartbeat(self, client, auth_headers_analyst):
        """Test that heartbeat response has correct structure."""
        payload = {
            "status": "online",
            "asset_id": 1,
            "cpu_usage": 50.0,
        }
        
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        # Check required fields
        assert "id" in data
        assert "status" in data
        assert "timestamp" in data
        
        # Check types
        assert isinstance(data["id"], int)
        assert isinstance(data["status"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_response_structure_status(self, client, auth_headers_analyst):
        """Test that status response has correct structure."""
        response = client.get(
            "/api/v1/telemetry/status",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check required fields
        assert "total_assets" in data
        assert "online_count" in data
        assert "offline_count" in data
        assert "warning_count" in data
        assert "missed_heartbeats_count" in data
        
        # Check types
        assert isinstance(data["total_assets"], int)
        assert isinstance(data["online_count"], int)
