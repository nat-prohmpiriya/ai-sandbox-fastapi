from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException
from src.models.user import User  # Beanie User model
from src.services.user import (
    get_user_by_uid,
    get_all_users,
    create_user,
    update_user,
    delete_user,
)

router: APIRouter = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[Dict[str, any]])
async def get_users() -> List[Dict[str, any]]:
    """Get all users from database"""
    users: List[User] = await get_all_users()
    return [user.model_dump() for user in users]

@router.get("/{uid}", response_model=Dict[str, any])
async def get_user(uid: str) -> Dict[str, any]:
    """Get a user by UID"""
    user: Optional[User] = await get_user_by_uid(uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.model_dump()

@router.post("/", response_model=Dict[str, any])
async def create_user_route(user_data: Dict[str, any]) -> Dict[str, any]:
    """Create a new user"""
    user: User = await create_user(user_data)
    return user.model_dump()

@router.put("/{uid}", response_model=Dict[str, any])
async def update_user_route(uid: str, user_data: Dict[str, any]) -> Dict[str, any]:
    """Update an existing user"""
    user: Optional[User] = await update_user(uid, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.model_dump()

@router.delete("/{uid}", response_model=Dict[str, str])
async def delete_user_route(uid: str) -> Dict[str, str]:
    """Delete a user by UID"""
    result: bool = await delete_user(uid)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}