from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field

class User(Document):
    uid: str = Field(...)
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    is_active: bool = True

    class Settings:
        name = "users"  # collection name in MongoDB