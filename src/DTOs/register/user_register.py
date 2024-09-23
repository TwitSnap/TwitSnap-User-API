from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    register_type : str
    username: str 
    email: str
    password: str
    phone: str
    country: str

