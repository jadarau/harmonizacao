from __future__ import annotations
import os
from typing import list, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Groq Configuration
    groq_api_key: str
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_default_model: str = "llama-3.3-70b-versatile"
    
    # Request Configuration
    request_timeout_s: float = 30.0
    http_max_retries: int = 2
    
    # CORS Configuration
    enable_cors: bool = True
    cors_allow_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()