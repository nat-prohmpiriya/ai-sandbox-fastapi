from typing import Any, Dict, Optional
from src.models.user import User

async def create_user(user_info: Dict[str, Any]) -> Dict[str, Any]:
    uid: str = user_info["uid"]
    user: Optional[User] = await User.find_one(User.uid == uid)
    if user is None:
        user = User(
            uid=uid,
            email=user_info.get("email"),
            display_name=user_info.get("name") or user_info.get("displayName"),
        )
        await user.insert()
    return user.model_dump()

async def get_user_uid(uid: str) -> Optional[User]:
    user: Optional[User] = await User.find_one(User.uid == uid)
    return user

async def update_user(uid: str, update_data: Dict[str, Any]) -> Optional[User]:
    user: Optional[User] = await User.find_one(User.uid == uid)
    if user:
        await user.update({"$set": update_data})
        return user
    return None

async def delete_user(uid: str) -> bool:
    user: Optional[User] = await User.find_one(User.uid == uid)
    if user:
        await user.delete()
        return True
    return False

async def list_users() -> list[User]:
    users: list[User] = await User.find_all().to_list()
    return users

