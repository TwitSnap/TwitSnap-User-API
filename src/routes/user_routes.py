from typing import Optional, List
from fastapi import APIRouter, Header, Query, Request, logger,status, Depends
from DTOs.auth.aurh_user_response import AuthUserResponse
from DTOs.backoffice.ban_user_request import BanUserRequest
from DTOs.user.update_user_form import UpdateUserForm
from DTOs.user.user_profile import UserProfile
from DTOs.user.user_profile_preview import UserProfilePreview
from controllers.user_controller import user_controller
from exceptions.bad_request_exception import BadRequestException
from config.settings import logger
user_router = APIRouter()

# routes for auth
@user_router.get("/auth", status_code = status.HTTP_200_OK, response_model = AuthUserResponse)
async def get_user_auth_status_by_email(email: str):
    return await user_controller.get_user_by(email)

# routes for users
@user_router.patch("/me", status_code= status.HTTP_200_OK, response_model= UserProfile, response_model_exclude_none=True)
async def edit_my_user (request: Request, user_update_form: UpdateUserForm = Depends(UpdateUserForm)):
    return await user_controller.edit_user_by_id(request ,user_update_form)

@user_router.get("/confirmation")
async def verify_register_pin(id: str, pin: str):
    return await user_controller.confirm_user(id, pin)

@user_router.post("/{id}/pin",)
async def refresh_register_pin(id: str):
    return await user_controller.refresh_register_pin(id)

@user_router.get("/{id}",status_code = status.HTTP_200_OK, response_model= UserProfile, response_model_exclude_none=True)
async def get_user_by_id ( id : str,  request: Request):
    return await user_controller.get_user_by_id(request ,id)

@user_router.get("/", response_model=List[UserProfilePreview],response_model_exclude_none= True, status_code=status.HTTP_200_OK)
async def get_users(username: Optional[str] = Query(None), offset: int = Query(0, ge=0),limit: int = Query(10, gt=0)):
    return await user_controller.get_users_by_username(username, offset, limit)



