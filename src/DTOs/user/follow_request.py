from pydantic import BaseModel


class FollowRequest(BaseModel):
    id: str
