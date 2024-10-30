from fastapi import APIRouter, status, Query
from DTOs.backoffice.ban_user_request import BanUserRequest
from controllers.user_controller import user_controller

from src.DTOs.user.user_profile import UserProfile

admin_router = APIRouter()


@admin_router.patch("/users/{id}/ban", status_code=status.HTTP_204_NO_CONTENT)
async def ban_user(id: str, req: BanUserRequest):
    return await user_controller.ban_user(id, req)


@admin_router.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserProfile, response_model_exclude_none=True)
async def get_user_by_id_for_admin(id: str):
    return await user_controller.get_user_by_id_admin(id)


@admin_router.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserProfile], response_model_exclude_none=True)
async def get_all_users(offset: int = Query(0, ge=0), limit: int = Query(10, gt=0)):
    return await user_controller.get_all_users(offset, limit)
