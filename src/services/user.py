from typing import Any, Dict, Optional, List
from datetime import datetime, timezone
from src.models.user import User
from beanie import PydanticObjectId

class UserService:
    @staticmethod
    async def create_user(user_info: Dict[str, Any]) -> Dict[str, Any]:
        uid: str = user_info["uid"]
        user: Optional[User] = await User.find_one(User.uid == uid)
        now: datetime = datetime.now(timezone.utc)
        if user is None:
            user = User(
                uid=uid,
                email=user_info.get("email"),
                display_name=user_info.get("name") or user_info.get("displayName"),
                created_at=now,
                updated_at=now,
            )
            await user.insert()
        else:
            user.updated_at = now
            await user.save()
        data: Dict[str, Any] = user.model_dump()
        if hasattr(user, "id") and user.id is not None:
            data["id"] = str(user.id)
        return data

    @staticmethod
    async def get_user(id: str) -> Optional[User]:
        try:
            object_id: PydanticObjectId = PydanticObjectId(id)
        except Exception:
            return None
        user: Optional[User] = await User.find_one(User.id == object_id, User.deleted_at == None)
        return user

    @staticmethod
    async def update_user(id: str, update_data: Dict[str, Any]) -> Optional[User]:
        try:
            object_id: PydanticObjectId = PydanticObjectId(id)
        except Exception:
            return None
        user: Optional[User] = await User.find_one(User.id == object_id, User.deleted_at == None)
        if user:
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.now(timezone.utc)
            await user.save()
            return user
        return None

    @staticmethod
    async def delete_user(id: str) -> bool:
        try:
            object_id: PydanticObjectId = PydanticObjectId(id)
        except Exception:
            return False
        user: Optional[User] = await User.find_one(User.id == object_id, User.deleted_at == None)
        if user:
            user.deleted_at = datetime.now(timezone.utc)
            await user.save()
            return True
        return False

    @staticmethod
    async def get_users() -> List[User]:
        users: List[User] = await User.find(User.deleted_at == None).to_list()
        return users