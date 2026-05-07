"""FastAPI dependencies for authentication and RBAC."""

import hmac
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.auth.service import decode_token
from app.schemas.user import TokenData
from app.db import get_db
from app.middleware.rate_limiter import agent_rate_limiter

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_current_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current authenticated user from JWT token (header or cookie). Returns None if no token."""
    if token is None:
        token = request.cookies.get("access_token")
    if token is None:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception

    # Fetch user from database
    user = db.query(User).filter(User.username == token_data.username).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise credentials_exception

    return user


async def verify_agent_secret(
    x_agent_secret: Optional[str] = Header(None, alias="X-Agent-Secret"),
) -> bool:
    """
    Verify agent secret from X-Agent-Secret header.

    Returns True if the agent secret is valid, raises 401 otherwise.
    """
    if x_agent_secret is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Agent secret required",
        )

    if not hmac.compare_digest(x_agent_secret or "", settings.AGENT_SECRET):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid agent secret",
        )

    return True


async def verify_agent_or_user(
    request: Request,
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme),
    x_agent_secret: Optional[str] = Header(None, alias="X-Agent-Secret"),
) -> dict:
    """
    Combined authentication: accepts either JWT user auth OR agent secret.

    Returns a dict with auth_type and user (if JWT auth).
    This dependency is for routes that accept both authentication methods.
    """
    # Try JWT auth first
    if token is not None:
        token_data = decode_token(token)
        if token_data and token_data.username:
            user = db.query(User).filter(User.username == token_data.username).first()
            if user and user.is_active:
                return {"auth_type": "user", "user": user}

    # Try agent secret
    if x_agent_secret is not None:
        if hmac.compare_digest(x_agent_secret, settings.AGENT_SECRET):
            return {"auth_type": "agent"}

    # Neither worked
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required: provide JWT token or X-Agent-Secret header",
    )


async def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user)
) -> User:
    """Check if current user is active. Raises 401 if not authenticated."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require admin role for access."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_analyst_or_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require analyst or admin role for access."""
    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst or admin access required"
        )
    return current_user


async def rate_limit_agent(request: Request) -> bool:
    """
    Rate limit dependency for agent endpoints based on client IP.
    
    Limits agents to 60 requests per minute per IP address.
    This protects against bruteforce attacks on AGENT_SECRET.
    
    Raises:
        HTTPException 429: If rate limit is exceeded
    """
    client_ip = request.client.host if request.client else "unknown"
    if not agent_rate_limiter.is_allowed(f"agent:{client_ip}"):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )
    return True
