from fastapi import APIRouter, HTTPException, status, Response
from DTOs.user_register import UserRegistration
from services.user_service import user_service
from DTOs.user_login import UserLogin

class SessionController:
    def __init__(self, user_service):
        self.user_service = user_service

    async def register(self, user_register_data: UserRegistration):
        try:
            user, password = await user_service.create_user(user_register_data)
            return (user, password)

        except HTTPException as e:
            raise HTTPException(self, status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(e)

    async def login(self, user_login_data: UserLogin):
        try:
            user = await user_service.get_user(user_login_data.mail)
            # apicall a auth user.id
            return user
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(e)

    async def login_google(self):
        return


session_controller = SessionController(user_service)

