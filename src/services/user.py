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