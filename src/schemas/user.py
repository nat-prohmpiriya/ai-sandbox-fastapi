from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserUpdateRequest(BaseModel):
    display_name: Optional[str] = None