from DTOs.register.google_register import GoogleRegister
from services.user_service import user_service
from DTOs.register.user_register import UserRegister
from DTOs.auth.auth_user_register import AuthUserRegister
from fastapi import Request, requests, status
from config.settings import oauth
from exceptions.conflict_exception import ConflictException
import httpx
class RegisterService:
    def __init__(self):
        self.service = user_service

    async def register(self, register_data: UserRegister):

        if await self.service.exists_user_by_email(register_data.email):
            raise ConflictException(f"The email address {register_data.email} is already registered.")
        
        user = await self.service.create_user(register_data)
        auth_user_register = AuthUserRegister(id = user.uid, password = register_data.password)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"https://twitsnap-auth-api.onrender.com/v1/auth/register",
                                            json = auth_user_register.model_dump())
            if response.status_code != status.HTTP_201_CREATED :
                raise(Exception("Error register user in auth service"))
            
        return user    
        
    
    async def register_with_google(self, token : GoogleRegister):
        user_info = await verify_google_token(token.token)
        if user_info is None:
            raise Exception("Invalid token")
        id = user_info['sub'] 
        email = user_info['email']     
        name = user_info['name']      

        if not self.service.exists_user_by_email (email):
            return await self.service.create_user_with_federated_identity(id, email, name)
        raise ConflictException(f"Google user with email {email} is already registered")

async def verify_google_token(token):
    try:
        response = await requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception:
        return None
    
register_service = RegisterService()