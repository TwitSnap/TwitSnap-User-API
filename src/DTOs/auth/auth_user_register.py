from pydantic import BaseModel
class AuthUserRegister(BaseModel):
    id: str
    password: str
