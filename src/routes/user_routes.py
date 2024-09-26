from fastapi import APIRouter, status, Depends
from controllers.user_controller import user_controller
from utils.decode_token import get_current_user, oauth2_scheme
from pydantic import BaseModel
from DTOs.user.edit_user import EditUser

user_router = APIRouter()

@user_router.get("/id", status_code = status.HTTP_200_OK)
async def get_user_id_by_email(email: str):
    return await user_controller.get_user_id_by(email)

@user_router.get("/me", status_code= status.HTTP_200_OK)
async def get_my_user (user_id: str = Depends(get_current_user)):
    return await user_controller.get_user_by_id(user_id)

@user_router.patch("/me", status_code= status.HTTP_200_OK)
async def edit_my_user (new_user_data: EditUser ,user_id: str = Depends(get_current_user)):
    return await user_controller.edit_user_by_id(new_user_data ,user_id)

@user_router.get("/{id}",status_code = status.HTTP_200_OK)
async def get_user_by_id ( id : str):
    return await user_controller.get_user_by_id(id)

@user_router.get("/", status_code= status.HTTP_200_OK)
async def get_all_users ():
    return await user_controller.get_all_users()
