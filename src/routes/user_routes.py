from typing import Optional, List
from fastapi import APIRouter, Header, Query, Request,status, Depends
from DTOs.user.update_user_form import UpdateUserForm
from DTOs.user.user_profile import UserProfile
from DTOs.user.user_profile_preview import UserProfilePreview
from controllers.user_controller import user_controller
from utils.get_current_user import get_current_user
from config.settings import logger
user_router = APIRouter()

@user_router.get("/id", status_code = status.HTTP_200_OK)
async def get_user_id_by_email(email: str):
    return await user_controller.get_user_id_by(email)

@user_router.get("/me", status_code= status.HTTP_200_OK, response_model= UserProfile, response_model_exclude_none=True)
async def get_my_user (request: Request):
    user_id = get_current_user(request)
    return await user_controller.get_user_by_id("me",user_id)

@user_router.patch("/me", status_code= status.HTTP_200_OK, response_model= UserProfile, response_model_exclude_none=True)
async def edit_my_user (request: Request, user_update_form: UpdateUserForm = Depends(UpdateUserForm),response_model= UserProfile, response_model_exclude_none=True):
    user_id = get_current_user(request)
    return await user_controller.edit_user_by_id(user_update_form, user_id)

@user_router.get("/{id}",status_code = status.HTTP_200_OK, response_model= UserProfile, response_model_exclude_none=True)
async def get_user_by_id ( id : str,  request: Request):
    user_id = get_current_user(request)
    return await user_controller.get_user_by_id(id, user_id)

@user_router.post("/{id}/pin",)
async def refresh_register_pin(id: str):
    return await user_controller.refresh_register_pin(id)

@user_router.post("/confirmation")
async def verify_register_pin(id: str, pin: str):
    return await user_controller.confirm_user(id, pin)

@user_router.patch("/{id}/ban")
async def ban_user(id: str):
    return await user_controller.ban_user(id)

@user_router.patch("/{id}/unban")
async def unban_user(id: str):
    return await user_controller.unban_user(id)

@user_router.get("/", response_model=List[UserProfilePreview],response_model_exclude_none= True, status_code=status.HTTP_200_OK)
async def get_users(username: Optional[str] = Query(None), offset: int = Query(0, ge=0),limit: int = Query(10, gt=0)):
    return await user_controller.get_users_by_username(username, offset, limit)
