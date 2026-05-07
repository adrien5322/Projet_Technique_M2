"""Tests for events module.

Tests cover:
- Event model
- Event schemas validation
- Event service functions
- Events API endpoints
- RBAC for events routes
- Agent authentication for event ingestion
"""

import pytest
from datetime import datetime, timedelta
from fastapi import status
from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.event import (
    EventCreate,
    EventResponse,
    EventListResponse,
    VALID_EVENT_TYPES,
    VALID_SEVERITIES,
)
from app.events.service import create_event, get_events, get_event_by_id


class TestEventModel:
    """Tests for Event model."""

    def test_create_event_model(self, db_session):
        """Test creating an Event instance."""
        event = Event(
            source_ip="192.168.1.100",
            event_type="network_scan",
            severity="high",
            raw_data={"detail": "Port scan detected"},
            asset_id=1,
        )
        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        assert event.id is not None
        assert event.source_ip == "192.168.1.100"
        assert event.event_type == "network_scan"
        assert event.severity == "high"
        assert event.raw_data == {"detail": "Port scan detected"}
        assert event.asset_id == 1
        assert event.timestamp is not None
        assert event.created_at is not None

    def test_event_repr(self, db_session):
        """Test Event __repr__ method."""
        event = Event(
            event_type="malware",
            severity="critical",
        )
        db_session.add(event)
        db_session.commit()

        repr_str = repr(event)
        assert "event_type=malware" in repr_str
        assert "severity=critical" in repr_str

    def test_event_with_nullable_fields(self, db_session):
        """Test creating event with only required fields."""
        event = Event(
            event_type="other",
            severity="low",
        )
        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        assert event.id is not None
        assert event.source_ip is None
        assert event.raw_data is None
        assert event.asset_id is None

    def test_event_all_event_types(self, db_session):
        """Test creating events with all valid event types."""
        for event_type in VALID_EVENT_TYPES:
            event = Event(event_type=event_type, severity="medium")
            db_session.add(event)
        db_session.commit()

        events = db_session.query(Event).all()
        assert len(events) == len(VALID_EVENT_TYPES)

    def test_event_all_severities(self, db_session):
        """Test creating events with all valid severities."""
        for severity in VALID_SEVERITIES:
            event = Event(event_type="other", severity=severity)
            db_session.add(event)
        db_session.commit()

        events = db_session.query(Event).all()
        assert len(events) == len(VALID_SEVERITIES)


class TestEventSchemas:
    """Tests for event Pydantic schemas."""

    def test_valid_event_create(self):
        """Test valid EventCreate schema."""
        data = {
            "source_ip": "10.0.0.1",
            "event_type": "brute_force",
            "severity": "high",
            "raw_data": {"attempts": 50, "target": "ssh"},
            "asset_id": 1,
        }
        schema = EventCreate(**data)

        assert schema.source_ip == "10.0.0.1"
        assert schema.event_type == "brute_force"
        assert schema.severity == "high"
        assert schema.asset_id == 1

    def test_event_create_minimal(self):
        """Test EventCreate with only required fields."""
        data = {"event_type": "other", "severity": "low"}
        schema = EventCreate(**data)

        assert schema.event_type == "other"
        assert schema.severity == "low"
        assert schema.source_ip is None
        assert schema.raw_data is None
        assert schema.asset_id is None

    def test_invalid_event_type(self):
        """Test validation with invalid event_type."""
        data = {"event_type": "invalid_type", "severity": "low"}

        with pytest.raises(ValueError) as exc_info:
            EventCreate(**data)

        assert "Event type must be one of" in str(exc_info.value)

    def test_invalid_severity(self):
        """Test validation with invalid severity."""
        data = {"event_type": "other", "severity": "extreme"}

        with pytest.raises(ValueError) as exc_info:
            EventCreate(**data)

        assert "Severity must be one of" in str(exc_info.value)

    def test_all_valid_event_types(self):
        """Test all valid event type values."""
        for event_type in VALID_EVENT_TYPES:
            data = {"event_type": event_type, "severity": "low"}
            schema = EventCreate(**data)
            assert schema.event_type == event_type

    def test_all_valid_severities(self):
        """Test all valid severity values."""
        for severity in VALID_SEVERITIES:
            data = {"event_type": "other", "severity": severity}
            schema = EventCreate(**data)
            assert schema.severity == severity

    def test_event_response_schema(self):
        """Test EventResponse schema structure."""
        now = datetime.utcnow()
        data = {
            "id": 1,
            "source_ip": "192.168.1.1",
            "event_type": "malware",
            "severity": "critical",
            "raw_data": {"file": "trojan.exe"},
            "asset_id": 5,
            "timestamp": now,
            "created_at": now,
        }
        schema = EventResponse(**data)

        assert schema.id == 1
        assert schema.event_type == "malware"
        assert schema.severity == "critical"

    def test_event_list_response_schema(self):
        """Test EventListResponse schema structure."""
        data = {
            "events": [],
            "total": 0,
            "page": 1,
            "page_size": 50,
        }
        schema = EventListResponse(**data)

        assert schema.events == []
        assert schema.total == 0
        assert schema.page == 1
        assert schema.page_size == 50

    def test_source_ip_max_length(self):
        """Test source_ip max length validation."""
        # IPv6 max length is 45 characters
        long_ip = "a" * 46
        data = {"event_type": "other", "severity": "low", "source_ip": long_ip}

        with pytest.raises(ValueError):
            EventCreate(**data)

    def test_missing_required_event_type(self):
        """Test that event_type is required."""
        with pytest.raises(ValueError):
            EventCreate(severity="low")

    def test_missing_required_severity(self):
        """Test that severity is required."""
        with pytest.raises(ValueError):
            EventCreate(event_type="other")


class TestEventService:
    """Tests for event service functions."""

    def test_create_event_service(self, db_session):
        """Test create_event service function."""
        event_data = EventCreate(
            source_ip="10.0.0.1",
            event_type="network_scan",
            severity="medium",
            raw_data={"ports": [22, 80, 443]},
            asset_id=1,
        )

        result = create_event(db_session, event_data)

        assert result.id is not None
        assert result.source_ip == "10.0.0.1"
        assert result.event_type == "network_scan"
        assert result.severity == "medium"
        assert result.raw_data == {"ports": [22, 80, 443]}
        assert result.asset_id == 1

    def test_get_events_basic(self, db_session):
        """Test get_events service function."""
        # Create test events
        for i in range(5):
            event = Event(
                event_type="network_scan",
                severity="low",
            )
            db_session.add(event)
        db_session.commit()

        events, total = get_events(db_session)

        assert total == 5
        assert len(events) == 5

    def test_get_events_with_pagination(self, db_session):
        """Test get_events with pagination."""
        for i in range(10):
            event = Event(event_type="other", severity="low")
            db_session.add(event)
        db_session.commit()

        events, total = get_events(db_session, skip=0, limit=3)

        assert total == 10
        assert len(events) == 3

    def test_get_events_filter_by_severity(self, db_session):
        """Test get_events filtered by severity."""
        db_session.add(Event(event_type="other", severity="low"))
        db_session.add(Event(event_type="other", severity="high"))
        db_session.add(Event(event_type="other", severity="critical"))
        db_session.commit()

        events, total = get_events(db_session, severity="high")

        assert total == 1
        assert events[0].severity == "high"

    def test_get_events_filter_by_event_type(self, db_session):
        """Test get_events filtered by event_type."""
        db_session.add(Event(event_type="network_scan", severity="low"))
        db_session.add(Event(event_type="brute_force", severity="medium"))
        db_session.add(Event(event_type="malware", severity="high"))
        db_session.commit()

        events, total = get_events(db_session, event_type="malware")

        assert total == 1
        assert events[0].event_type == "malware"

    def test_get_events_filter_both(self, db_session):
        """Test get_events filtered by both severity and event_type."""
        db_session.add(Event(event_type="network_scan", severity="low"))
        db_session.add(Event(event_type="network_scan", severity="high"))
        db_session.add(Event(event_type="malware", severity="high"))
        db_session.commit()

        events, total = get_events(db_session, severity="high", event_type="network_scan")

        assert total == 1
        assert events[0].event_type == "network_scan"
        assert events[0].severity == "high"

    def test_get_event_by_id(self, db_session):
        """Test get_event_by_id service function."""
        event = Event(event_type="malware", severity="critical")
        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        result = get_event_by_id(db_session, event.id)

        assert result is not None
        assert result.id == event.id
        assert result.event_type == "malware"

    def test_get_event_by_id_not_found(self, db_session):
        """Test get_event_by_id with non-existent ID."""
        result = get_event_by_id(db_session, 9999)

        assert result is None

    def test_get_events_empty(self, db_session):
        """Test get_events with no data."""
        events, total = get_events(db_session)

        assert total == 0
        assert events == []


class TestEventsRoutes:
    """Tests for events API endpoints."""

    def test_post_event_with_user_auth(self, client, auth_headers_analyst):
        """Test POST /api/v1/events with JWT user auth."""
        payload = {
            "source_ip": "192.168.1.50",
            "event_type": "brute_force",
            "severity": "high",
            "raw_data": {"attempts": 100},
            "asset_id": 1,
        }

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["event_type"] == "brute_force"
        assert data["severity"] == "high"
        assert data["source_ip"] == "192.168.1.50"
        assert "id" in data
        assert "timestamp" in data

    def test_post_event_with_agent_auth(self, client, agent_secret_headers):
        """Test POST /api/v1/events with agent secret auth."""
        payload = {
            "event_type": "network_scan",
            "severity": "medium",
            "source_ip": "10.0.0.5",
        }

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=agent_secret_headers,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["event_type"] == "network_scan"
        assert data["severity"] == "medium"

    def test_post_event_without_auth(self, client):
        """Test POST /api/v1/events without authentication."""
        payload = {"event_type": "other", "severity": "low"}

        response = client.post("/api/v1/events", json=payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_event_invalid_agent_secret(self, client):
        """Test POST /api/v1/events with invalid agent secret."""
        payload = {"event_type": "other", "severity": "low"}
        headers = {"X-Agent-Secret": "wrong-secret"}

        response = client.post("/api/v1/events", json=payload, headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_event_invalid_event_type(self, client, auth_headers_analyst):
        """Test POST /api/v1/events with invalid event_type."""
        payload = {"event_type": "invalid", "severity": "low"}

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_post_event_invalid_severity(self, client, auth_headers_analyst):
        """Test POST /api/v1/events with invalid severity."""
        payload = {"event_type": "other", "severity": "extreme"}

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_post_event_minimal(self, client, auth_headers_analyst):
        """Test POST /api/v1/events with minimal data."""
        payload = {"event_type": "other", "severity": "low"}

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["event_type"] == "other"
        assert data["severity"] == "low"
        assert data["source_ip"] is None

    def test_get_events_list(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/events list."""
        for i in range(5):
            event = Event(event_type="network_scan", severity="low")
            db_session.add(event)
        db_session.commit()

        response = client.get("/api/v1/events", headers=auth_headers_analyst)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "events" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert data["total"] == 5
        assert len(data["events"]) == 5

    def test_get_events_list_without_auth(self, client):
        """Test GET /api/v1/events without authentication."""
        response = client.get("/api/v1/events")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_events_list_with_pagination(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/events with pagination."""
        for i in range(10):
            event = Event(event_type="other", severity="low")
            db_session.add(event)
        db_session.commit()

        response = client.get(
            "/api/v1/events?page=1&page_size=3",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 10
        assert len(data["events"]) == 3
        assert data["page"] == 1
        assert data["page_size"] == 3

    def test_get_events_list_filter_severity(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/events filtered by severity."""
        db_session.add(Event(event_type="other", severity="low"))
        db_session.add(Event(event_type="other", severity="high"))
        db_session.add(Event(event_type="other", severity="critical"))
        db_session.commit()

        response = client.get(
            "/api/v1/events?severity=high",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["events"][0]["severity"] == "high"

    def test_get_events_list_filter_event_type(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/events filtered by event_type."""
        db_session.add(Event(event_type="network_scan", severity="low"))
        db_session.add(Event(event_type="malware", severity="high"))
        db_session.add(Event(event_type="brute_force", severity="medium"))
        db_session.commit()

        response = client.get(
            "/api/v1/events?event_type=malware",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 1
        assert data["events"][0]["event_type"] == "malware"

    def test_get_event_by_id(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/events/{event_id}."""
        event = Event(event_type="malware", severity="critical", source_ip="10.0.0.1")
        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        response = client.get(
            f"/api/v1/events/{event.id}",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == event.id
        assert data["event_type"] == "malware"
        assert data["severity"] == "critical"

    def test_get_event_by_id_not_found(self, client, auth_headers_analyst):
        """Test GET /api/v1/events/{event_id} with non-existent ID."""
        response = client.get(
            "/api/v1/events/9999",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Event not found"

    def test_get_event_by_id_without_auth(self, client):
        """Test GET /api/v1/events/{event_id} without authentication."""
        response = client.get("/api/v1/events/1")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_event_all_event_types(self, client, auth_headers_analyst):
        """Test POST /api/v1/events with all valid event types."""
        for event_type in ["network_scan", "brute_force", "malware",
                           "unauthorized_access", "data_exfiltration", "other"]:
            payload = {"event_type": event_type, "severity": "medium"}
            response = client.post(
                "/api/v1/events",
                json=payload,
                headers=auth_headers_analyst,
            )
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json()["event_type"] == event_type

    def test_post_event_all_severities(self, client, auth_headers_analyst):
        """Test POST /api/v1/events with all valid severities."""
        for severity in ["low", "medium", "high", "critical"]:
            payload = {"event_type": "other", "severity": severity}
            response = client.post(
                "/api/v1/events",
                json=payload,
                headers=auth_headers_analyst,
            )
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json()["severity"] == severity

    def test_post_event_with_admin(self, client, auth_headers_admin):
        """Test POST /api/v1/events with admin auth."""
        payload = {"event_type": "malware", "severity": "critical"}

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=auth_headers_admin,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_response_structure_event(self, client, auth_headers_analyst):
        """Test that event response has correct structure."""
        payload = {
            "event_type": "network_scan",
            "severity": "high",
            "source_ip": "192.168.1.1",
            "raw_data": {"scan_type": "syn"},
            "asset_id": 1,
        }

        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert "id" in data
        assert "timestamp" in data
        assert "created_at" in data
        assert "event_type" in data
        assert "severity" in data
        assert "source_ip" in data
        assert "raw_data" in data
        assert "asset_id" in data

        assert isinstance(data["id"], int)
        assert isinstance(data["event_type"], str)
        assert isinstance(data["severity"], str)

    def test_get_events_empty_list(self, client, auth_headers_analyst):
        """Test GET /api/v1/events with no events."""
        response = client.get("/api/v1/events", headers=auth_headers_analyst)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert data["events"] == []

    def test_get_events_page_out_of_range(self, client, auth_headers_analyst, db_session):
        """Test GET /api/v1/events with page beyond available data."""
        for i in range(3):
            db_session.add(Event(event_type="other", severity="low"))
        db_session.commit()

        response = client.get(
            "/api/v1/events?page=10",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 3
        assert len(data["events"]) == 0

    def test_get_events_invalid_page(self, client, auth_headers_analyst):
        """Test GET /api/v1/events with invalid page number."""
        response = client.get(
            "/api/v1/events?page=0",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_events_invalid_page_size(self, client, auth_headers_analyst):
        """Test GET /api/v1/events with invalid page_size."""
        response = client.get(
            "/api/v1/events?page_size=0",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_events_page_size_too_large(self, client, auth_headers_analyst):
        """Test GET /api/v1/events with page_size exceeding max."""
        response = client.get(
            "/api/v1/events?page_size=500",
            headers=auth_headers_analyst,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
