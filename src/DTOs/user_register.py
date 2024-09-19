from pydantic import BaseModel

class UserRegistration(BaseModel):
    username: str
    mail: str
    password: str
    phone: str
    country: str