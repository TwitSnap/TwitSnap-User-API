# src/controllers/register_controller.py
from fastapi import APIRouter, HTTPException, status
from DTOs.register_request import UserRegistration
from services.user_service import user_service

class RegisterController:
    def __init__(self, user_service):
        self.router = APIRouter()
        self.user_service = user_service

        @self.router.post("/register", status_code = status.HTTP_201_CREATED)
        async def register_user(user: UserRegistration):
            try:
                user = await self.user_service.create_user(user)
                return user # uuid,password
                # apicall a auth
            except HTTPException as e:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            except Exception as e:
                print(e)


register_router = RegisterController(user_service).router

