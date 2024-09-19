from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    mail: str
    password: str
    phone: str
    country: str