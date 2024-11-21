from pydantic import BaseModel
from typing import Optional


class UserProfilePreview(BaseModel):
    uid: Optional[str]
    username: Optional[str] = None
    photo: Optional[str] = None
    description: Optional[str] = None
    is_followed_by_me: Optional[bool] = None
