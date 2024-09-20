from fastapi import Request, HTTPException, status, Response
from DTOs.user_register import UserRegister
from services.session_service import session_service
from DTOs.user_login import UserLogin

class SessionController:
    def __init__(self, session_service):
        self.session_service = session_service

    async def register(self, user_register_data: UserRegister):
        try:
            return await session_service.register(user_register_data)
        except HTTPException as e:
            raise HTTPException(self, status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(e)

    async def login(self, user_login_data: UserLogin):
        try:
            return await session_service.login(user_login_data)
        
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            print(e)
    
    async def login_google(self, request: Request):
        return await session_service.login_google(request)

    async def auth_google(self, request: Request):
        return await session_service.auth_google(request)


session_controller = SessionController(session_service)

