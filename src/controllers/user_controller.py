from fastapi import HTTPException, status, Response
from DTOs.register.user_register import UserRegister
from services.user_service import user_service

class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    async def register(self, user_register_data: UserRegister):
        try:
            return await self.user_service.register(user_register_data)
        except HTTPException as e:
            raise HTTPException(self, status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(e)
    
    async def get_user_id_by(self, type : str , identifier : str):
        try:
            if type == 'email':
                user = await self.user_service.get_user_id_by_email(identifier)
            else:
                raise HTTPException(status_code=400, detail="Invalid search type")
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_user_by_id (self, id : str):
        try:
            return await self.user_service.get_user_by_id(id)
        except HTTPException as e:
            raise HTTPException(self, status_code=e.status_code, detail=e.detail)
        
    async def get_all_users (self,):
        try:
            return await self.user_service.get_all_users()
        except HTTPException as e:
            raise HTTPException(self, status_code=e.status_code, detail=e.detail)
        
user_controller = UserController(user_service)

