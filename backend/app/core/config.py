"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Stefan's Task Manager"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = ""
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "*"  # Allow all origins for development
    ]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    
    class Config:
        env_file = BASE_DIR / ".env"
        case_sensitive = True

settings = Settings()