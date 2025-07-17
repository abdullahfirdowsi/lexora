from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lexora API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./lexora.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ElevenLabs API
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Hugging Face API
    HUGGINGFACE_API_KEY: Optional[str] = None
    SUPRATH_LIPSYNC_URL: str = "https://suprath-lipsync.hf.space/run/predict"
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

