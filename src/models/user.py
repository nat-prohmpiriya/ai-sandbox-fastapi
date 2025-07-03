from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field

class User(Document):
    uid: str = Field(...)
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Settings:
        name = "users"  # collection name in MongoDB