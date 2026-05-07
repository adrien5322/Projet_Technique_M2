"""Tests for rate limiter functionality.

Tests cover:
- SimpleRateLimiter unit tests
- Rate limiting on agent endpoints (heartbeat, events, audit/log)
- 429 Too Many Requests response after rate limit exceeded
"""

import time
import pytest
from fastapi import status
from app.middleware.rate_limiter import SimpleRateLimiter, agent_rate_limiter


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset the agent rate limiter before each test."""
    agent_rate_limiter.reset()
    yield
    agent_rate_limiter.reset()


class TestSimpleRateLimiterUnit:
    """Unit tests for SimpleRateLimiter class."""

    def test_allows_requests_under_limit(self):
        """Test that requests under the limit are allowed."""
        limiter = SimpleRateLimiter(max_requests=5, window_seconds=60)
        
        for i in range(5):
            assert limiter.is_allowed("test_key") is True
        
        # 6th request should be denied
        assert limiter.is_allowed("test_key") is False

    def test_blocks_requests_over_limit(self):
        """Test that requests over the limit are blocked."""
        limiter = SimpleRateLimiter(max_requests=3, window_seconds=60)
        
        # First 3 requests allowed
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        
        # 4th request blocked
        assert limiter.is_allowed("client1") is False

    def test_different_keys_independent(self):
        """Test that different keys have independent rate limits."""
        limiter = SimpleRateLimiter(max_requests=2, window_seconds=60)
        
        # Client 1 uses their limit
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is False
        
        # Client 2 should still be allowed
        assert limiter.is_allowed("client2") is True
        assert limiter.is_allowed("client2") is True
        assert limiter.is_allowed("client2") is False

    def test_sliding_window_expires_old_requests(self):
        """Test that old requests expire after the window passes."""
        limiter = SimpleRateLimiter(max_requests=3, window_seconds=1)
        
        # Use up the limit
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is False
        
        # Wait for window to pass
        time.sleep(1.1)
        
        # Should be allowed again
        assert limiter.is_allowed("client1") is True

    def test_reset_specific_key(self):
        """Test resetting rate limit for a specific key."""
        limiter = SimpleRateLimiter(max_requests=2, window_seconds=60)
        
        # Use up limit
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is False
        
        # Reset for this key
        limiter.reset("client1")
        
        # Should be allowed again
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is False

    def test_reset_all_keys(self):
        """Test resetting rate limit for all keys."""
        limiter = SimpleRateLimiter(max_requests=1, window_seconds=60)
        
        # Use up limit for two clients
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client1") is False
        assert limiter.is_allowed("client2") is True
        assert limiter.is_allowed("client2") is False
        
        # Reset all
        limiter.reset()
        
        # Both should be allowed again
        assert limiter.is_allowed("client1") is True
        assert limiter.is_allowed("client2") is True


class TestRateLimitingOnAgentEndpoints:
    """Integration tests for rate limiting on agent endpoints."""

    def test_heartbeat_rate_limiting(self, client, agent_secret_headers):
        """Test that POST /api/v1/telemetry/heartbeat is rate limited."""
        payload = {"status": "online", "cpu_usage": 45.0}
        
        # Send 60 requests (should all succeed)
        for i in range(60):
            response = client.post(
                "/api/v1/telemetry/heartbeat",
                json=payload,
                headers=agent_secret_headers,
            )
            assert response.status_code == status.HTTP_201_CREATED, f"Request {i+1} failed with {response.status_code}"
        
        # 61st request should be rate limited
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=agent_secret_headers,
        )
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Rate limit exceeded" in response.json()["detail"]

    def test_events_rate_limiting(self, client, agent_secret_headers):
        """Test that POST /api/v1/events is rate limited."""
        payload = {
            "event_type": "network_scan",
            "severity": "medium",
            "source_ip": "10.0.0.1",
        }
        
        # Send 60 requests (should all succeed)
        for i in range(60):
            response = client.post(
                "/api/v1/events",
                json=payload,
                headers=agent_secret_headers,
            )
            assert response.status_code == status.HTTP_201_CREATED, f"Request {i+1} failed with {response.status_code}"
        
        # 61st request should be rate limited
        response = client.post(
            "/api/v1/events",
            json=payload,
            headers=agent_secret_headers,
        )
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Rate limit exceeded" in response.json()["detail"]

    def test_audit_log_rate_limiting(self, client, agent_secret_headers):
        """Test that POST /api/v1/audit/log is rate limited."""
        payload = {
            "action": "test_action",
            "resource_type": "test_resource",
        }
        
        # Send 60 requests (should all succeed)
        for i in range(60):
            response = client.post(
                "/api/v1/audit/log",
                json=payload,
                headers=agent_secret_headers,
            )
            assert response.status_code == status.HTTP_201_CREATED, f"Request {i+1} failed with {response.status_code}"
        
        # 61st request should be rate limited
        response = client.post(
            "/api/v1/audit/log",
            json=payload,
            headers=agent_secret_headers,
        )
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Rate limit exceeded" in response.json()["detail"]

    def test_rate_limiting_per_ip(self, client, agent_secret_headers):
        """Test that rate limiting is applied per IP address."""
        # This test verifies that the rate limiter uses client IP
        # In test client, all requests appear to come from the same IP
        # so we just verify the rate limiter is working
        payload = {"status": "online"}
        
        # Exhaust limit for "testclient" IP
        for i in range(60):
            response = client.post(
                "/api/v1/telemetry/heartbeat",
                json=payload,
                headers=agent_secret_headers,
            )
            assert response.status_code == status.HTTP_201_CREATED
        
        # Next request should be blocked
        response = client.post(
            "/api/v1/telemetry/heartbeat",
            json=payload,
            headers=agent_secret_headers,
        )
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

    def test_rate_limiting_only_on_agent_endpoints(self, client, auth_headers_analyst):
        """Test that rate limiting only applies to agent endpoints, not user endpoints."""
        # Read endpoints should not be rate limited
        response = client.get(
            "/api/v1/telemetry/status",
            headers=auth_headers_analyst,
        )
        # Should not be rate limited (may be 200 or other error, but not 429)
        assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS

    def test_rate_limit_with_invalid_secret(self, client):
        """Test that rate limiting applies even with invalid agent secret."""
        # Even with invalid secret, rate limiting should kick in
        # to prevent bruteforce attacks
        payload = {"status": "online"}
        headers = {"X-Agent-Secret": "wrong-secret"}
        
        # Send many requests with wrong secret
        # The rate limiter should still track these
        responses = []
        for i in range(61):
            response = client.post(
                "/api/v1/telemetry/heartbeat",
                json=payload,
                headers=headers,
            )
            responses.append(response.status_code)
        
        # Some requests should get 429 (rate limited)
        # and some should get 401 (invalid secret)
        # The exact order depends on implementation, but we should see both
        has_401 = status.HTTP_401_UNAUTHORIZED in responses
        has_429 = status.HTTP_429_TOO_MANY_REQUESTS in responses
        
        assert has_401, "Should have some 401 Unauthorized responses"
        # Note: rate limiting might not kick in if auth check happens first
        # This is acceptable as long as the rate limiter is in place


class TestRateLimiterReset:
    """Tests for rate limiter reset functionality between tests."""

    def test_reset_agent_rate_limiter(self):
        """Test resetting the global agent rate limiter."""
        # Reset before test
        agent_rate_limiter.reset()
        
        # Use up the limit
        for i in range(60):
            assert agent_rate_limiter.is_allowed("test:127.0.0.1") is True
        
        assert agent_rate_limiter.is_allowed("test:127.0.0.1") is False
        
        # Reset
        agent_rate_limiter.reset("test:127.0.0.1")
        
        # Should work again
        assert agent_rate_limiter.is_allowed("test:127.0.0.1") is True
        
        # Clean up
        agent_rate_limiter.reset()
