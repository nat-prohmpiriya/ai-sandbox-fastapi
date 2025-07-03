# src/models/chat.py
from typing import Optional, List
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field
from bson import ObjectId
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):  # Embedded model
    id: str = Field(default_factory=lambda: str(ObjectId()))
    role: MessageRole
    content: str
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class ChatSession(Document):  # Main document
    user_id: str
    title: Optional[str] = None
    is_active: bool = True
    
    messages: List[ChatMessage] = Field(default_factory=list)
    
    message_count: int = 0
    last_message_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Settings:
        name = "chat_sessions"