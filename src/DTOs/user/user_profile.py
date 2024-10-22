from typing import Optional

from pydantic import BaseModel

from DTOs.user.user_profile_preview import UserProfilePreview

class UserProfile(BaseModel):
    uid: Optional[str] 
    username: Optional[str] = None
    photo: Optional[str] = None
    country: Optional[str] = None 
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    amount_of_followers: Optional[int] = None
    amount_of_following : Optional[int] = None
    verified: Optional[bool] = None
    is_follwed_by_me: Optional[bool] = None
    followers: Optional[list[UserProfilePreview]] = None
    following: Optional[list[UserProfilePreview]] = None