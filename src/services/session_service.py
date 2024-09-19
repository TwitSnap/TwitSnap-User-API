from services.user_service import user_service
from DTOs.user_register import UserRegister
from DTOs.user_login import UserLogin
from DTOs.user_register_auth import UserRegisterAuth
from DTOs.user_login_auth import UserLoginAuth
# import httpx

class SessionService:
    def __init__(self):
        self.service = user_service

    async def register(self, user_data: UserRegister):
        user = await self.service.create_user(user_data)
        user_register_auth = UserRegisterAuth(user_id = user.uid, password = user_data.password)

        return user_register_auth

    async def login(self, user_data: UserLogin):
        user_login_auth = UserLoginAuth(mail = user_data.mail, password = user_data.password)
        user_id = await self.service.get_user_id_by_mail(user_login_auth.mail)
        return user_id

        # async with httpx.AsyncClient() as client:
        #     url = "auth"
        #     auth_response = await client.post(url, json={mail:{user_login_auth.mail}})

    async def login_google(self):
            return

session_service = SessionService()