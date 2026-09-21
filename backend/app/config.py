from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CyberAudit360"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = "sqlite:///./cyberaudit360.db"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"  # Should be overridden by environment variable
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    
    # Options
    DEMO_MODE: bool = False
    LIVE_INTELLIGENCE: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
