from pydantic import BaseModel, Field
from typing import Optional

class UserProfile(BaseModel):
    uid: Optional[str] 
    username: Optional[str]
