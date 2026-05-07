"""Authentication routes: login, token generation."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.schemas.user import UserLogin, Token, UserResponse
from app.auth.service import create_access_token, authenticate_user
from app.auth.dependencies import get_db, get_current_active_user
from app.models.user import User
from app.audit import service as audit_service

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db),
    request: Request = None,
) -> dict:
    """
    Authenticate user and return JWT token.
    
    - **username**: User's username
    - **password**: User's password
    """
    # Authenticate against real database
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    
    client_ip = request.client.host if request and request.client else None
    
    if not user:
        # Audit failed login attempt
        audit_service.log_action(
            db=db,
            action="login_failed",
            resource_type="user",
            resource_id=user_credentials.username,
            details={"reason": "invalid_credentials"},
            ip_address=client_ip,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token with real user data
    user_data = {
        "sub": user.username,
        "role": user.role
    }
    access_token = create_access_token(data=user_data)
    
    # Audit successful login
    audit_service.log_action(
        db=db,
        action="login_success",
        resource_type="user",
        resource_id=str(user.id),
        details={"username": user.username, "role": user.role},
        ip_address=client_ip,
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current authenticated user information.
    
    Requires authentication via JWT token.
    """
    return current_user
