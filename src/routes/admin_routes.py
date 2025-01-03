from fastapi import APIRouter, status, Query, Request
from controllers.user_controller import user_controller
from dtos.user.user_profile import UserProfile
from typing import Optional

from dtos.user.admin_get_all_users import GetUsers

admin_router = APIRouter()


@admin_router.post("/users/{id}/ban", status_code=status.HTTP_204_NO_CONTENT)
async def ban_or_unban_user(id: str):
    return await user_controller.ban_or_unban_user(id)


@admin_router.get("/users/metrics", status_code=status.HTTP_200_OK)
async def get_metrics(
    metric_type: Optional[str] = Query(
        None,
        description="Type of metric: registration, banned, country_distribution, if not provided, all metrics will be returned",
    )
):
    return await user_controller.get_user_metrics(metric_type)


@admin_router.get(
    "/users/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    response_model_exclude_none=True,
)
async def get_user_by_id_for_admin(request:Request, id: str):
    return await user_controller.get_user_by_id_admin(request, id)


@admin_router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=GetUsers,
    response_model_exclude_none=True,
)
async def get_all_users(request: Request, offset: int = Query(0, ge=0), limit: int = Query(10, gt=0), is_banned: Optional[bool] = None):
    return await user_controller.get_all_users(request, offset, limit, is_banned)
