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

    class Config:
        env_file = "src/config/.env.local"

settings = Settings()