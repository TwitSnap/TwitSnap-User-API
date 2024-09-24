from DTOs.register.user_register import UserRegister
from services.user_service import user_service

class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    async def register(self, user_register_data: UserRegister):
        return await self.user_service.register(user_register_data)
    
    async def get_user_id_by(self, type : str , identifier : str):
        if type == 'email':
            return await self.user_service.get_user_id_by_email(identifier)
        
    async def get_user_by_id (self, id : str):
        return await self.user_service.get_user_by_id(id)

    async def get_all_users (self,):
        return await self.user_service.get_all_users()
    
user_controller = UserController(user_service)

