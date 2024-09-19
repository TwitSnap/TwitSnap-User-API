from pydantic import BaseModel

class UserLoginAuth(BaseModel):
    mail: str
    password: str