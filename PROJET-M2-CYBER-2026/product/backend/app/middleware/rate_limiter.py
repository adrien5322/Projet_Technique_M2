"""
Simple in-memory rate limiter for DAR-Cyber.

Provides rate limiting without external dependencies (Redis, etc.)
using a sliding window algorithm.
"""

import time
from collections import defaultdict
from threading import Lock
from typing import Optional


class SimpleRateLimiter:
    """
    Simple in-memory rate limiter using sliding window algorithm.
    
    Thread-safe implementation using a Lock for concurrent access.
    """
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()
    
    def is_allowed(self, key: str) -> bool:
        """
        Check if a request with the given key is allowed.
        
        Args:
            key: Identifier for the client (e.g., IP address)
            
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        now = time.time()
        with self._lock:
            # Clean old entries outside the window
            cutoff = now - self.window_seconds
            self._requests[key] = [t for t in self._requests[key] if t > cutoff]
            
            # Check if limit exceeded
            if len(self._requests[key]) >= self.max_requests:
                return False
            
            # Record this request
            self._requests[key].append(now)
            return True
    
    def reset(self, key: Optional[str] = None) -> None:
        """
        Reset rate limit for a specific key or all keys.
        
        Args:
            key: If provided, reset only this key. Otherwise reset all.
        """
        with self._lock:
            if key:
                self._requests.pop(key, None)
            else:
                self._requests.clear()


# Global instance for agent endpoints
# Limits to 60 requests per minute per IP
agent_rate_limiter = SimpleRateLimiter(max_requests=60, window_seconds=60)
