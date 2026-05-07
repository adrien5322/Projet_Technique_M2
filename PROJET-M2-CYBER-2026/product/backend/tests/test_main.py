"""Tests for main application."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct info."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "app_name" in data
        assert "version" in data
        assert "docs" in data
        assert "redoc" in data
        # Check that health endpoint is documented (not in root response)
        # The root response has "health" key pointing to the health endpoint path
        assert "health" not in data  # health is not in root response
        # But /health endpoint should exist
        health_response = client.get("/health")
        assert health_response.status_code == 200
