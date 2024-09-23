from fastapi import APIRouter, Request
from controllers.register_controller import register_controller
from DTOs.register.user_register import UserRegister


register_router = APIRouter()

@register_router.post("/")
async def register(user_register_data: UserRegister, request : Request):
    return await register_controller.register(user_register_data, request)

@register_router.get("/google")
async def register_with_google(request: Request):
    return await register_controller.register_with_google(request)

@register_router.get("/google/callback")
async def register_with_google_callback(request :Request):
    return await register_controller.register_with_google_callback(request)
