from typing import Optional
from pydantic import BaseModel
class GoogleRegister(BaseModel): 
    token : str = None
    uid: Optional [str] = None
    username: Optional [str] = None
    email: Optional [str] = None
    photo: Optional [str] = None
