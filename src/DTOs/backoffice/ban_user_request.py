from pydantic import BaseModel


class BanUserRequest(BaseModel):
    is_banned: bool