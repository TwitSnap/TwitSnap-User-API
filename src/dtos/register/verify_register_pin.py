from pydantic import BaseModel


class VerifyRegisterPin(BaseModel):
    id: str
    pin: str
