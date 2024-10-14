from pydantic import BaseModel

class GeneratedPinResponse(BaseModel):
    pin_ttl: str    