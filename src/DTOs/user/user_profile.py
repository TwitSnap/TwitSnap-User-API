from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    uid: Optional[str] 
    username: Optional[str]
    photo: Optional[str]
