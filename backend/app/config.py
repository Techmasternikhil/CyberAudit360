from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import secrets
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "CyberAudit360"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./cyberaudit360.db"
    
    # Security: Generate a cryptographically secure random key if not provided via environment
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173", 
        "http://127.0.0.1:5173", 
        "http://localhost:3000"
    ]
    
    # Options
    DEMO_MODE: bool = False
    LIVE_INTELLIGENCE: bool = False

settings = Settings()
