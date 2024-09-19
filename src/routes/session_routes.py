from fastapi import APIRouter, Depends
from controllers.session_controller import session_controller
from DTOs.user_login import UserLogin
from DTOs.user_register import UserRegister


session_router = APIRouter()

@session_router.post("/register")
async def register(user_register_data: UserRegister):
    return await session_controller.register(user_register_data)

@session_router.post("/login")
async def login(user_login_data: UserLogin):
    return await session_controller.login(user_login_data)

@session_router.get("/login/google")
async def login_google():
    return await session_controller.login_google()

