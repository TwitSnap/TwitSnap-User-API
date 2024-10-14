from typing import Optional, List
from fastapi import APIRouter, Query,status, Depends
from DTOs.user.update_user_form import UpdateUserForm
from DTOs.user.user_profile import UserProfile
from controllers.user_controller import user_controller
from utils.decode_token import get_current_user

user_router = APIRouter()

@user_router.get("/id", status_code = status.HTTP_200_OK)
async def get_user_id_by_email(email: str):
    return await user_controller.get_user_id_by(email)

@user_router.get("/me", status_code= status.HTTP_200_OK)
async def get_my_user (user_id: str = Depends(get_current_user)):
    return await user_controller.get_user_by_id(user_id)

@user_router.patch("/me", status_code= status.HTTP_200_OK)
async def edit_my_user (user_update_form: UpdateUserForm = Depends(UpdateUserForm), user_id: str = Depends(get_current_user),):
    return await user_controller.edit_user_by_id(user_update_form, user_id)

@user_router.get("/{id}",status_code = status.HTTP_200_OK)
async def get_user_by_id ( id : str):
    return await user_controller.get_user_by_id(id)

@user_router.post("{id}/pin")
async def refresh_register_pin(user_id: str):
    return await user_controller.refresh_register_pin(user_id)

@user_router.post("/confirmation")
async def verify_register_pin(user_id: str, pin: str):
    return await user_controller.confirm_user(user_id, pin)

@user_router.get("/", response_model=List[UserProfile])
async def get_users(username: Optional[str] = Query(None), offset: int = Query(0, ge=0),limit: int = Query(10, gt=0)):
    return await user_controller.get_users_by_username(username, offset, limit)
