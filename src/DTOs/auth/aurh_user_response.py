from pydantic import BaseModel


class AuthUserResponse(BaseModel):
    uid: str
    is_banned: bool