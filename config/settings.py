from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import Optional

class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Application
    APP_NAME: str = "PermitAI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT != "production"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/permitai_db"
    )
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    DATABASE_ECHO: bool = DEBUG
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_CACHE_TTL: int = 3600
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: list = ["http://localhost:8501", "https://yourdomain.com"]
    
    # AI Models
    AI_MODEL_TYPE: str = "local"
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    CLAUDE_API_KEY: Optional[str] = os.getenv("CLAUDE_API_KEY")
    LOCAL_MODEL_PATH: str = "./models"
    
    # File Upload
    MAX_UPLOAD_MB: int = 200
    SUPPORTED_FORMATS: set = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}
    UPLOAD_TEMP_DIR: str = "./temp_uploads"
    
    # OCR
    OCR_ENABLED: bool = True
    OCR_LANGUAGE: str = "eng"
    
    # Features
    FEATURE_ADVANCED_AI: bool = True
    FEATURE_REPORTS: bool = True
    FEATURE_COLLABORATION: bool = True
    FEATURE_ANALYTICS: bool = True
    
    # Disciplines
    DISCIPLINES: list = [
        "Architecture",
        "Structural",
        "Electrical",
        "Mechanical",
        "Plumbing",
        "Civil",
        "Fire Protection",
        "Landscape"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
