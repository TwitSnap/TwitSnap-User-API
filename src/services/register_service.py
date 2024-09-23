from services.user_service import user_service
from DTOs.register.user_register import UserRegister
from DTOs.auth.auth_user_register import AuthUserRegister
from fastapi import Request
from fastapi.responses import RedirectResponse
from config.settings import oauth

class RegisterService:
    def __init__(self):
        self.service = user_service

    async def register(self, register_data: UserRegister, request: Request):
        if register_data.register_type == "google":
            return await self.register_with_google(request)
        else:
            user = await self.service.create_user(register_data)
            auth_user_register = AuthUserRegister(id = user.uid, password = register_data.password)
            return auth_user_register

    async def register_with_google(self, request : Request):
        redirect_uri = "http://localhost:8006/v1/register/google/callback"
        return await oauth.google.authorize_redirect(request, redirect_uri)

    
    async def register_with_google_callback(self, request: Request):
        token = await oauth.google.authorize_access_token(request)
        # user_info = await oauth.google.parse_id_token(request, token)

        # google_id = user_info.get("sub")
        # email = user_info.get("email")
        # username = user_info.get("name")
        # await self.service.create_user(google_id, email, username)

        return RedirectResponse(url="https://x.com") # login en el front

register_service = RegisterService()