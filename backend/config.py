import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "ReguDraft AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # API Gateway Configurations
    API_V1_STR: str = "/api/v1"
    
    # Security Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super_secret_signing_key_for_regudraft_ai_change_in_production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database Configurations
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./regudraft.db")
    
    # Redis Cache and Broker Configurations
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Vector Database Configurations
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY", None)
    
    # Storage Configuration (S3 Compatible)
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "regudraft-documents")
    S3_ACCESS_KEY_ID: Optional[str] = os.getenv("S3_ACCESS_KEY_ID", "mock_access_key")
    S3_SECRET_ACCESS_KEY: Optional[str] = os.getenv("S3_SECRET_ACCESS_KEY", "mock_secret_key")
    S3_ENDPOINT_URL: Optional[str] = os.getenv("S3_ENDPOINT_URL", "http://localhost:9000")  # MinIO default
    
    # LLM Configurations
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "mock_openai_key")
    OPENAI_MODEL: str = "gpt-4-turbo"
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", None)
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


    model_config = {
        "extra": "ignore",
        "case_sensitive": True,
        "env_file": ".env"
    }

settings = Settings()
