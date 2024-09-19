from pydantic import BaseModel

class UserRegisterAuth(BaseModel):
    user_id: str
    password: str