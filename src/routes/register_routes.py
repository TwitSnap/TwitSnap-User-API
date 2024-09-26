from fastapi import APIRouter, Request, status
from controllers.register_controller import register_controller
from DTOs.register.user_register import UserRegister
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


register_router = APIRouter()

@register_router.post("/", status_code=status.HTTP_201_CREATED)
async def register(user_register_data: UserRegister):
    return await register_controller.register(user_register_data)

@register_router.get("/google")
async def register_with_google(request : Request):
    return await register_controller.register_with_google(request)


