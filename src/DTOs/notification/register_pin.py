from pydantic import BaseModel

class RegisterPin(BaseModel):
    type: str
    params: dict
    notifications: dict
