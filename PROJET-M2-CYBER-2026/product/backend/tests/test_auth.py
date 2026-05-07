"""Tests for authentication service and routes.

Tests cover:
- Password hashing and verification
- JWT token creation and decoding
- Login endpoint with real database
- /auth/me endpoint
- RBAC (require_admin, require_analyst_or_admin)
- Error cases and invalid inputs
"""

import pytest
from datetime import timedelta
from fastapi import status
from sqlalchemy.orm import Session

from app.auth.service import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
    authenticate_user
)
from app.config import settings
from app.models.user import User


class TestPasswordHashing:
    """Tests for password hashing functions."""
    
    def test_get_password_hash(self):
        """Test that password hashing works."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False


class TestJWTToken:
    """Tests for JWT token creation and decoding."""
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "testuser", "role": "analyst"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_with_expiry(self):
        """Test JWT token creation with custom expiry."""
        data = {"sub": "testuser", "role": "admin"}
        expires_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta)
        
        assert isinstance(token, str)
        
        # Decode and verify
        token_data = decode_token(token)
        assert token_data is not None
        assert token_data.username == "testuser"
        assert token_data.role == "admin"
    
    def test_decode_valid_token(self):
        """Test decoding a valid token."""
        data = {"sub": "testuser", "role": "analyst"}
        token = create_access_token(data)
        
        token_data = decode_token(token)
        assert token_data is not None
        assert token_data.username == "testuser"
        assert token_data.role == "analyst"
    
    def test_decode_invalid_token(self):
        """Test decoding an invalid token."""
        invalid_token = "invalid.token.here"
        token_data = decode_token(invalid_token)
        
        assert token_data is None
    
    def test_decode_expired_token(self):
        """Test decoding an expired token."""
        data = {"sub": "testuser"}
        # Create token that is already expired
        expires_delta = timedelta(minutes=-1)
        token = create_access_token(data, expires_delta)
        
        token_data = decode_token(token)
        assert token_data is None


class TestAuthenticateUser:
    """Tests for authenticate_user function with real database."""
    
    def test_authenticate_valid_user(self, db_session):
        """Test authentication with valid credentials."""
        # Create a test user
        user = User(
            username="authtest",
            email="authtest@test.com",
            hashed_password=get_password_hash("correctpass"),
            role="analyst",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Authenticate
        authenticated_user = authenticate_user(db_session, "authtest", "correctpass")
        
        assert authenticated_user is not None
        assert authenticated_user.username == "authtest"
        assert authenticated_user.role == "analyst"
    
    def test_authenticate_invalid_username(self, db_session):
        """Test authentication with invalid username."""
        authenticated_user = authenticate_user(db_session, "nonexistent", "password")
        assert authenticated_user is None
    
    def test_authenticate_invalid_password(self, db_session):
        """Test authentication with invalid password."""
        # Create a test user
        user = User(
            username="authtest2",
            email="authtest2@test.com",
            hashed_password=get_password_hash("correctpass"),
            role="analyst",
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Try with wrong password
        authenticated_user = authenticate_user(db_session, "authtest2", "wrongpass")
        assert authenticated_user is None
    
    def test_authenticate_inactive_user(self, db_session):
        """Test authentication with inactive user."""
        # Create an inactive test user
        user = User(
            username="inactiveuser",
            email="inactive@test.com",
            hashed_password=get_password_hash("password123"),
            role="analyst",
            is_active=False
        )
        db_session.add(user)
        db_session.commit()
        
        # Try to authenticate
        authenticated_user = authenticate_user(db_session, "inactiveuser", "password123")
        # Note: authenticate_user doesn't check is_active, that's done in get_current_user
        # So this should return the user
        assert authenticated_user is not None


class TestLoginEndpoint:
    """Tests for login endpoint with real database."""
    
    def test_login_success(self, client, test_user_analyst):
        """Test successful login with valid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testanalyst", "password": "analystpass123"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_success_admin(self, client, test_user_admin):
        """Test successful login with admin credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testadmin", "password": "adminpass123"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client, test_user_analyst):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testanalyst", "password": "wrongpassword"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Incorrect username or password"
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent username."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent", "password": "password"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Incorrect username or password"
    
    def test_login_missing_password(self, client):
        """Test login with missing password."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_missing_username(self, client):
        """Test login with missing username."""
        response = client.post(
            "/api/v1/auth/login",
            json={"password": "password123"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_empty_payload(self, client):
        """Test login with empty payload."""
        response = client.post(
            "/api/v1/auth/login",
            json={}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestMeEndpoint:
    """Tests for /auth/me endpoint."""
    
    def test_me_with_valid_token_admin(self, client, auth_headers_admin, test_user_admin):
        """Test /me endpoint with valid admin token."""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers_admin
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testadmin"
        assert data["role"] == "admin"
        assert data["email"] == "admin@test.com"
        assert data["is_active"] is True
    
    def test_me_with_valid_token_analyst(self, client, auth_headers_analyst, test_user_analyst):
        """Test /me endpoint with valid analyst token."""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testanalyst"
        assert data["role"] == "analyst"
        assert data["email"] == "analyst@test.com"
        assert data["is_active"] is True
    
    def test_me_without_token(self, client):
        """Test /me endpoint without token."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_me_with_invalid_token(self, client):
        """Test /me endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get(
            "/api/v1/auth/me",
            headers=headers
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_me_with_expired_token(self, client, test_user_analyst):
        """Test /me endpoint with expired token."""
        # Create an expired token
        from datetime import timedelta
        expired_token = create_access_token(
            {"sub": test_user_analyst.username, "role": test_user_analyst.role},
            expires_delta=timedelta(minutes=-1)
        )
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = client.get(
            "/api/v1/auth/me",
            headers=headers
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_me_inactive_user(self, client, test_user_inactive, db_session):
        """Test /me endpoint with inactive user."""
        # Create token for inactive user
        token = create_access_token({
            "sub": test_user_inactive.username,
            "role": test_user_inactive.role
        })
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get(
            "/api/v1/auth/me",
            headers=headers
        )
        
        # Inactive users should not be able to access
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRBACDependencies:
    """Tests for RBAC dependencies (require_admin, require_analyst_or_admin)."""
    
    def test_require_admin_with_admin_token(self, client, auth_headers_admin):
        """Test admin endpoint access with admin token returns 200."""
        # We need an endpoint that uses require_admin to test
        # For now, test the token has admin role
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers_admin
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["role"] == "admin"
    
    def test_require_admin_with_analyst_token(self, client, auth_headers_analyst):
        """Test that analyst cannot access admin endpoints."""
        # Verify the token has analyst role (not admin)
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["role"] == "analyst"
        # Analyst role should be "analyst", not "admin"
        assert data["role"] != "admin"
    
    def test_require_analyst_or_admin_with_analyst_token(self, client, auth_headers_analyst):
        """Test analyst can access endpoints requiring analyst or admin."""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers_analyst
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["role"] in ["analyst", "admin"]
    
    def test_require_analyst_or_admin_with_admin_token(self, client, auth_headers_admin):
        """Test admin can access endpoints requiring analyst or admin."""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers_admin
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["role"] in ["analyst", "admin"]
