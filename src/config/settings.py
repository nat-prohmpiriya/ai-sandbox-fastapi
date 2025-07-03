from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool
    host: str
    port: int

    mongodb_url: str
    db_name: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    backend_cors_origins: List[str]
    firebase_credential_path: str
    google_api_key: Optional[str] = None  # Optional, can be set in .env.local

    class Config:
        env_file = "src/config/.env.local"

settings = Settings()