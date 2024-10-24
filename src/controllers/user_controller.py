from fastapi import Request
from fastapi.exceptions import RequestValidationError
from DTOs.backoffice.ban_user_request import BanUserRequest
from DTOs.register.user_register import UserRegister
from DTOs.user.edit_user import EditUser
from DTOs.user.update_user_form import UpdateUserForm
from exceptions.bad_request_exception import BadRequestException
from services.user_service import user_service
from exceptions.exception_handler import ExceptionHandler
from config.settings import logger

class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    async def register(self, user_register_data: UserRegister):
        try:
            return await self.user_service.register(user_register_data)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
    
    async def get_user_by(self, email: str):
        try:
            return await self.user_service.get_user_by_email(email)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
        
# endpoints that requires user_id from header
    async def get_user_by_id(self, request:Request, id: str): # type: ignore
        try:
            my_uid: str | None = self.get_current_user(request)
            if id == 'me' or id == my_uid:
                logger.debug(f"Getting my user with id: {my_uid}")
                return await self.user_service.get_my_user(my_uid)
            logger.debug(f"Getting user with id: {id}")
            return await self.user_service.get_user_by_id(id, my_uid)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def edit_user_by_id(self,request: Request,update_form: UpdateUserForm):
        try:
            my_uid: str | None = self.get_current_user(request)

            new_user_data = EditUser(username=update_form.username, phone=update_form.phone, country=update_form.country, description=update_form.description)
            if update_form.photo and not update_form.photo.filename.endswith((".jpg", ".jpeg", ".png")):
                logger.debug(f"Received file with content type {update_form.photo.content_type} - Only images are supported")
                raise RequestValidationError(f"Received file with content type {update_form.photo.content_type} - Only images are supported")
            return await self.user_service.edit_user_by_id(new_user_data, update_form.photo, my_uid)
        except Exception as e:
            return ExceptionHandler.handle_exception(e, request)
    
    async def get_users_by_username(self, username: str,offset: int , limit: int ):
        try:
            return await self.user_service.get_users_by_username(username,offset,limit)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
        
    async def refresh_register_pin(self, user_id: str):
        try:
            return await self.user_service.generate_register_pin(user_id)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
        
    async def confirm_user(self, user_id: str, pin: str):
        try:
            return await self.user_service.confirm_user(user_id, pin)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
    
    async def ban_user(self, user_id: str, req: BanUserRequest):
        try:
            return await self.user_service.ban_user(user_id, req)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
    
    async def get_user_by_id_admin(self, user_id: str):
        try:
            return await self.user_service.get_user_by_id_admin(user_id)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
        
    async def get_all_users(self, offset: int, limit: int):
        try:
            return await self.user_service.get_all_users(offset, limit)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)
    
    def get_current_user(self, req: Request):
        user_id = req.headers.get("user_id")
        logger.debug(f"User id found in headers: {user_id}")
        if user_id is None:
            raise BadRequestException(detail= "User id not found in headers")
        return user_id
user_controller = UserController(user_service)

