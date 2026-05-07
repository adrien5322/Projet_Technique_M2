"""Application configuration using Pydantic Settings."""

from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "DAR-Cyber"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database (required - no default with real credentials)
    DATABASE_URL: Optional[str] = None
    
    # JWT Security (required - no default for security)
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Agent Authentication (required - no default for security)
    AGENT_SECRET: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS - Restrictive defaults for security (localhost only for dev)
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: List[str] = ["Authorization", "Content-Type", "Accept"]
    
    # Nmap settings
    NMAP_TIMEOUT: int = 120
    NMAP_MAX_NETWORK_SIZE: int = 24  # CIDR prefix min (i.e. /24)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Raise error if required env vars are missing
        extra = "ignore"


settings = Settings()
