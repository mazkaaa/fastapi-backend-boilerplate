from functools import lru_cache
from typing import List, Optional

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    app_name: str = Field(default="FastAPI Boilerplate")
    environment: str = Field(default="development", description="Environment name (development|staging|production)")
    debug: bool = Field(default=True)
    version: str = Field(default="0.1.0")

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    # CORS
    cors_allow_origins: List[AnyHttpUrl] | List[str] = Field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: List[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: List[str] = Field(default_factory=lambda: ["*"])

    # Sentry / telemetry (placeholder)
    sentry_dsn: Optional[AnyHttpUrl] = None

    # OpenAPI
    docs_url: str = Field(default="/docs")
    redoc_url: str = Field(default="/redoc")
    openapi_url: str = Field(default="/openapi.json")

    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), env_prefix="APP_", case_sensitive=False)


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
