from fastapi import Request, HTTPException
from DTOs.register.user_register import UserRegister
from services.register_service import register_service
from exceptions.exception_handler import ExceptionHandler
class RegisterController:
    def __init__(self, register_service):
        self.register_service = register_service

    async def register(self, user_register_data: UserRegister, request: Request):
        try:
            return await self.register_service.register(user_register_data, request )
        except Exception as e:
             return await ExceptionHandler.handle_exception(e)
        
    async def register_with_google(self, request : Request):
        try:
            return await self.register_service.register_with_google(request)
        except Exception as e:
             return await ExceptionHandler.handle_exception(e)

    async def register_with_google_callback(self, request : Request):
        try:
            return await self.register_service.register_with_google_callback(request)
        except Exception as e:
             return await ExceptionHandler.handle_exception(e)

register_controller = RegisterController(register_service)

