from fastapi import APIRouter, status
from controllers.user_controller import user_controller

user_router = APIRouter()

@user_router.get("/id", status_code = status.HTTP_200_OK)
async def get_user_id(search_type: str, value: str):
    return await user_controller.get_user_id_by(search_type, value)

@user_router.get("/{id}", status_code = status.HTTP_200_OK)
async def get_user_by_id ( id : str):
    return await user_controller.get_user_by_id(id)

@user_router.get("/", status_code= status.HTTP_200_OK)
async def get_all_users ():
    return await user_controller.get_all_users()
