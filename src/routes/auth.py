from fastapi import APIRouter, Request
from src.schemas.auth import FirebaseVerifyResponse

router: APIRouter = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/firebase/verify", response_model=FirebaseVerifyResponse)
def firebase_verify(request: Request) -> FirebaseVerifyResponse:
    user_info: dict = request.state.user
    return FirebaseVerifyResponse(
        message=f"Firebase verification successful for {user_info.get('uid')}",
        uid=user_info.get("uid"),
        email=user_info.get("email"),
        display_name=user_info.get("name") or user_info.get("displayName")
    )