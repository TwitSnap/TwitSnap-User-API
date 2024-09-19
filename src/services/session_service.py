from src.services.user_service import user_service
from DTOs.user_register import UserRegister
from DTOs.user_login import UserLogin

class SessionService:
    def __init__(self):
        self.service = user_service

    async def register(self, user_register_data: UserRegister):
        (uuid, password) = await self.service.create_user(user_register_data)
        return (uuid, password)

    async def login(self, user_login_data: UserLogin):

        return await (user_login_data)

    async def login_google(self):
            return
