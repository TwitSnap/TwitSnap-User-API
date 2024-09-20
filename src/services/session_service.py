from services.user_service import user_service
from DTOs.user_register import UserRegister
from DTOs.user_login import UserLogin
from DTOs.user_register_auth import UserRegisterAuth
from DTOs.user_login_auth import UserLoginAuth
from fastapi import Request
from fastapi.responses import RedirectResponse
from config.db import oauth
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

    async def login_google(self, request: Request):
        redirect_uri = "http://localhost:8006/login/google/callback"
        return await oauth.google.authorize_redirect(request, redirect_uri)

    async def auth_google(self, request: Request):
        token = await oauth.google.authorize_access_token(request)

        return RedirectResponse(url="https://x.com") # devolver jwt token con los datos


session_service = SessionService()