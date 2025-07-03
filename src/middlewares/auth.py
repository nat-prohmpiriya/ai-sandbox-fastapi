from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from typing import Callable, Awaitable
from src.services.auth import verify_firebase_token
from src.services.user import UserService
import uuid
from typing import Any

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]) -> Any:
        request_id: str = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id

        id_token: str = request.headers.get("authorization", "").replace("Bearer ", "")
        if not id_token:
            raise HTTPException(status_code=401, detail="Missing Firebase token")
        try:
            user_info: dict = verify_firebase_token(id_token)
            await UserService.create_user(user_info)
            request.state.user = user_info
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid Firebase token")
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response