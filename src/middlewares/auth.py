from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from typing import Callable, Awaitable
from src.services.auth import verify_firebase_token

from typing import Any

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]) -> Any:
        id_token: str = request.headers.get("authorization", "").replace("Bearer ", "")
        if not id_token:
            raise HTTPException(status_code=401, detail="Missing Firebase token")
        try:
            user_info: dict = verify_firebase_token(id_token)
            request.state.user = user_info
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")
        response = await call_next(request)
        return response