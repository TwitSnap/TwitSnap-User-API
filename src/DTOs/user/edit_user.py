from pydantic import BaseModel, Field
from typing import Optional

class EditUser(BaseModel): 
    username: Optional[str] = Field (min_length = 3, max_length = 20) = None
    phone: Optional [str] = None
    country: Optional [str] = None
    description: Optional [str] = None