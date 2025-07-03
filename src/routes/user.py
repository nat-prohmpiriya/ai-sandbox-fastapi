from typing import List
from fastapi import APIRouter, HTTPException
from src.models.user import User
from src.services.user import UserService
from src.schemas.user import UserResponse, UserUpdateRequest

router: APIRouter = APIRouter(prefix="/users", tags=["users"])

## ------------------------------------------------------------------
def user_to_schema(user: User | None) -> UserResponse:
    """Convert a User model instance to a UserResponse schema instance"""
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    data: dict = user.model_dump()
    # Convert id (ObjectId) to string if present
    if "id" in data and data["id"] is not None:
        data["id"] = str(data["id"])
    return UserResponse.model_validate(data)

## ------------------------------------------------------------------
@router.get("/", response_model=List[UserResponse])
async def get_users() -> List[UserResponse]:
    """Get all users from database"""
    users: List[User] = await UserService.get_users()
    return [user_to_schema(user) for user in users]

## ------------------------------------------------------------------
@router.get("/{id}", response_model=UserResponse)
async def get_user(id: str) -> UserResponse:
    """Get a user by ObjectId"""
    user: User | None = await UserService.get_user(id)
    return user_to_schema(user)

## ------------------------------------------------------------------
@router.put("/{id}", response_model=UserResponse)
async def update_user_route(id: str, user_data: UserUpdateRequest) -> UserResponse:
    """Update an existing user (partial update supported)"""
    update_dict = user_data.model_dump(exclude_unset=True)
    user: User | None = await UserService.update_user(id, update_dict)
    return user_to_schema(user)

## ------------------------------------------------------------------
@router.delete("/{id}", response_model=dict)
async def delete_user_route(id: str) -> dict:
    """Delete a user by ObjectId (soft delete)"""
    result: bool = await UserService.delete_user(id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}