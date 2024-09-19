from pydantic import BaseModel

class UserLogin(BaseModel):
    mail: str
    password: str