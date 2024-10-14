from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from DTOs.register.user_register import UserRegister
from DTOs.user.edit_user import EditUser
from DTOs.user.update_user_form import UpdateUserForm
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
            return await ExceptionHandler.handle_exception(e)
    
    async def get_user_id_by(self, email: str):
        try:
            return await self.user_service.get_user_id_by_email(email)
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
        
    async def get_user_by_id(self, id: str):
        try:
            return await self.user_service.get_user_by_id(id)
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
                
    async def edit_user_by_id(self, update_form: UpdateUserForm, id: str):
        try:
            new_user_data = EditUser(username=update_form.username, phone=update_form.phone, country=update_form.country, description=update_form.description)
            if update_form.photo and not update_form.photo.filename.endswith((".jpg", ".jpeg", ".png")):
                logger.debug(f"Received file with content type {update_form.photo.content_type} - Only images are supported")
                raise RequestValidationError(f"Received file with content type {update_form.photo.content_type} - Only images are supported")
            return await self.user_service.edit_user_by_id(new_user_data, update_form.photo, id)
        except Exception as e:
            return await ExceptionHandler.handle_exception(e, request = Request)
    
    async def get_users_by_username(self, username: str,offset: int , limit: int ):
        try:
            return await self.user_service.get_users_by_username(username,offset,limit)
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
        
    async def refresh_register_pin(self, user_id: str):
        try:
            return await self.user_service.generate(user_id)
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
        
    async def confirm_user(self, user_id: str, pin: str):
        try:
            return await self.user_service.confirm_user(user_id, pin)
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
        
user_controller = UserController(user_service)
