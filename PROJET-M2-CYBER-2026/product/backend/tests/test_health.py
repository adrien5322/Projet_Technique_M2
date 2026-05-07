"""Tests for health endpoint."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check_status(self):
        """Test health endpoint returns status 200."""
        response = client.get("/health")
        
        assert response.status_code == 200
    
    def test_health_check_response(self):
        """Test health endpoint returns correct data."""
        response = client.get("/health")
        data = response.json()
        
        # Status can be "healthy" or "degraded" depending on database connectivity
        assert data["status"] in ["healthy", "degraded"]
        assert "app_name" in data
        assert "version" in data
        assert "database" in data
    
    def test_health_check_method_not_allowed(self):
        """Test health endpoint only accepts GET."""
        response = client.post("/health")
        
        assert response.status_code == 405  # Method not allowed
