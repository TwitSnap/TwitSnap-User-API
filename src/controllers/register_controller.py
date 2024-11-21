from dtos.register.google_register import GoogleRegister
from dtos.register.user_register import UserRegister
from services.register_service import register_service
from exceptions.exception_handler import ExceptionHandler


class RegisterController:
    def __init__(self, register_service):
        self.register_service = register_service

    async def register(self, user_register_data: UserRegister):
        try:
            return await self.register_service.register(user_register_data)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def register_with_google(self, token: GoogleRegister):
        try:
            return await self.register_service.register_with_google(token)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)


register_controller = RegisterController(register_service)
