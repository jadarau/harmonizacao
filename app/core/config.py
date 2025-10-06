from __future__ import annotations
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator

class AppSettings(BaseSettings):
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    groq_base_url: str = Field(default="https://api.groq.com/openai/v1", env="GROQ_BASE_URL")
    default_model: str = Field(default="llama-3.3-70b-versatile", env="GROQ_DEFAULT_MODEL")
    request_timeout_s: float = Field(30.0, env="REQUEST_TIMEOUT_S")
    max_retries: int = Field(2, env="HTTP_MAX_RETRIES")
    enable_cors: bool = Field(True, env="ENABLE_CORS")
    cors_allow_origins: List[str] = Field(default_factory=lambda: ["*"])

    @field_validator("cors_allow_origins", mode="before")
    def parse_cors_allow_origins(cls, v: Union[str, List[str], None]) -> List[str]:
        if v is None:
            return []
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    return [i.strip() for i in v.split(",")]
            return [i.strip() for i in v.split(",")]
        return v

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",  # Para evitar erro com variáveis extras no .env
    }

settings = AppSettings()