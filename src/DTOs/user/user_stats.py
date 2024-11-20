from typing import Optional
from pydantic import BaseModel


class UserStats(BaseModel):
    followers_gained: Optional[int]
    following_gained: Optional[int]
