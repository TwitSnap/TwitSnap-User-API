from typing import Optional
from fastapi import Form, UploadFile


class UpdateUserForm:
    def __init__(
        self,
        username: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        country: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        photo: Optional[UploadFile] = None,
        interests: Optional[list[str]] = Form(None),
        device_token: Optional[str] = Form(None),
    ):

        self.username = username
        self.phone = phone
        self.country = country
        self.interests = interests
        self.description = description
        self.photo = photo
        self.device_token = device_token