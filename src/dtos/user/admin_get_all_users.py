from pydantic import BaseModel
from typing import Optional

from dtos.user.user_profile import UserProfile


class GetUsers(BaseModel):
    total_users: Optional[int] = None
    users: Optional[list[UserProfile]] = None