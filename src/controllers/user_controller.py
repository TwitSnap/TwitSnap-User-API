from DTOs.register.user_register import UserRegister
from DTOs.user.edit_user import EditUser
from services.user_service import user_service
from exceptions.exception_handler import ExceptionHandler

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

    async def get_all_users(self):
        try:
            return await self.user_service.get_all_users()
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
        
    async def edit_user_by_id(self, req: EditUser, id: str):
        try:
            return await self.user_service.edit_user_by_id(req, id)
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
    
    async def delete_all_users(self):
        try:
            return await self.user_service.delete_all_users()
        except Exception as e:
            return await ExceptionHandler.handle_exception(e)
        
user_controller = UserController(user_service)
