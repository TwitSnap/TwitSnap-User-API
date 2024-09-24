from services.user_service import user_service
from DTOs.register.user_register import UserRegister
from DTOs.auth.auth_user_register import AuthUserRegister
from fastapi import Request
from fastapi.responses import RedirectResponse
from config.settings import oauth
from exceptions.conflict_exception import ConflictException
class RegisterService:
    def __init__(self):
        self.service = user_service

    async def register(self, register_data: UserRegister, request: Request):

        if register_data.register_type == "google":
            return await self.register_with_google(request)

        if await self.service.exists_user_by_email(register_data.email):
            raise ConflictException(f"The email address {register_data.email} is already registered.")
        else:            
            user = await self.service.create_user(register_data)
            auth_user_register = AuthUserRegister(id = user.uid, password = register_data.password)
            return auth_user_register

    async def register_with_google(self, request : Request):
        redirect_uri = "http://localhost:8006/api/v1/register/google/callback"
        return await oauth.google.authorize_redirect(request, redirect_uri)

    
    async def register_with_google_callback(self, request: Request):
        token = await oauth.google.authorize_access_token(request)

        google_id = token['userinfo'].get("sub")
        email = token['userinfo'].get("email")
        username = token['userinfo'].get("name")

        if not self.service.exists_user_by_email (email) :
            await self.service.create_user_with_federated_identity(google_id, email, username)
        
        return RedirectResponse(url="https://x.com") # login en el front

register_service = RegisterService()