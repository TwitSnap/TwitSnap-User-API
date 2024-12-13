from dtos.register.google_register import GoogleRegister
from dtos.register.user_register import UserRegister
from services.register_service import register_service
from fastapi import Request
from exceptions.exception_handler import ExceptionHandler
from config.settings import logger
from exceptions.no_auth_exception import UnauthorizedException
from external.twitsnap_service import twitsnap_service


class RegisterController:
    def __init__(self, register_service):
        self.register_service = register_service

    async def register(self, user_register_data: UserRegister):
        try:
            return await self.register_service.register(user_register_data)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def register_with_google(self, request:Request,token: GoogleRegister):
        try:
            api_key = self.get_api_key_from_header(request)
            if api_key:
                await self.validate_api_key(api_key)
            return await self.register_service.register_with_google(token)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    def get_api_key_from_header(self, req: Request):
        api_key = req.headers.get("api_key")
        logger.debug(f"Api key found in headers: {api_key}")
        if api_key is None:
           logger.error("Api key not found in headers")
           return None
        return api_key

    async def validate_api_key(self, api_key):
        if api_key:
            res = await twitsnap_service.verify_api_key(api_key)
            if res["isValid"] == False:
                raise UnauthorizedException(detail="Invalid API key")

register_controller = RegisterController(register_service)
