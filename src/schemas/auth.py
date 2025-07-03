from pydantic import BaseModel
from typing import Optional

class FirebaseVerifyResponse(BaseModel):
    message: str
    uid: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None
    