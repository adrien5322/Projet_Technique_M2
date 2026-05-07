"""Pytest configuration and fixtures for DAR-Cyber backend tests.

This module provides:
- Test database setup with SQLite in-memory database
- FastAPI TestClient with overridden dependencies
- User fixtures for authentication tests
- JWT token helpers
"""

import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# Load test environment variables before importing app modules
from dotenv import load_dotenv
test_env_path = Path(__file__).parent.parent / ".env.test"
if test_env_path.exists():
    load_dotenv(dotenv_path=test_env_path)

from app.main import app
from app.db import get_db
from app.models import Base
from app.config import Settings
from app.auth.service import get_password_hash, create_access_token
from app.models.user import User

# Test database setup - use SQLite in-memory for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    """Override get_db dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    yield session
    session.close()
    
    # Clean up - drop all tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Test client with overridden database dependency."""
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear overrides after test
    app.dependency_overrides.clear()
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user_admin(db_session):
    """Create an admin user for testing."""
    user = User(
        username="testadmin",
        email="admin@test.com",
        hashed_password=get_password_hash("adminpass123"),
        full_name="Test Admin",
        role="admin",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_analyst(db_session):
    """Create an analyst user for testing."""
    user = User(
        username="testanalyst",
        email="analyst@test.com",
        hashed_password=get_password_hash("analystpass123"),
        full_name="Test Analyst",
        role="analyst",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_inactive(db_session):
    """Create an inactive user for testing."""
    user = User(
        username="testinactive",
        email="inactive@test.com",
        hashed_password=get_password_hash("inactivepass123"),
        full_name="Test Inactive",
        role="analyst",
        is_active=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_token(test_user_admin):
    """Generate JWT token for admin user."""
    return create_access_token({
        "sub": test_user_admin.username,
        "role": test_user_admin.role
    })


@pytest.fixture
def analyst_token(test_user_analyst):
    """Generate JWT token for analyst user."""
    return create_access_token({
        "sub": test_user_analyst.username,
        "role": test_user_analyst.role
    })


@pytest.fixture
def auth_headers_admin(admin_token):
    """Return authorization headers with admin token."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def auth_headers_analyst(analyst_token):
    """Return authorization headers with analyst token."""
    return {"Authorization": f"Bearer {analyst_token}"}


@pytest.fixture
def agent_secret_headers():
    """Return headers with agent secret authentication."""
    return {"X-Agent-Secret": "test-agent-secret-change-me"}
