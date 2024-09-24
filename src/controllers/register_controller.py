from fastapi import Request, HTTPException
from DTOs.register.user_register import UserRegister
from services.register_service import register_service

class RegisterController:
    def __init__(self, register_service):
        self.register_service = register_service

    async def register(self, user_register_data: UserRegister, request: Request):
            return await self.register_service.register(user_register_data, request )
    
    async def register_with_google(self, request : Request):
            return await self.register_service.register_with_google(request)
    
    async def register_with_google_callback(self, request : Request):
            return await self.register_service.register_with_google_callback(request)

register_controller = RegisterController(register_service)

