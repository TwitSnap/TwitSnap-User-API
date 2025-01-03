from fastapi import APIRouter, status, Request
from dtos.register.google_register import GoogleRegister
from dtos.user.user_profile import UserProfile
from controllers.register_controller import register_controller
from dtos.register.user_register import UserRegister

register_router = APIRouter()


@register_router.post(
    "/",
    response_model=UserProfile,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_register_data: UserRegister):
    return await register_controller.register(user_register_data)


@register_router.post("/google", status_code=status.HTTP_201_CREATED)
async def register_with_google(request:Request, token: GoogleRegister):
    return await register_controller.register_with_google(request, token)
