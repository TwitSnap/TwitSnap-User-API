from typing import Optional, List
from dtos.register.verify_register_pin import VerifyRegisterPin
from fastapi import APIRouter, Query, Request, status, Depends
from dtos.auth.aurh_user_response import AuthUserResponse
from dtos.user.follow_request import FollowRequest
from dtos.user.update_user_form import UpdateUserForm
from dtos.user.user_profile import UserProfile
from dtos.user.user_profile_preview import UserProfilePreview
from controllers.user_controller import user_controller
from dtos.user.user_stats import UserStats

user_router = APIRouter()

# routes for auth


@user_router.get(
    "/auth", status_code=status.HTTP_200_OK, response_model=AuthUserResponse
)
async def get_user_auth_status_by_email(request: Request, email: str):
    return await user_controller.get_user_by(request, email)


# routes for users


@user_router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    response_model_exclude_unset=True,
)
async def edit_my_user(
    request: Request, user_update_form: UpdateUserForm = Depends(UpdateUserForm)
):
    return await user_controller.edit_user_by_id(request, user_update_form)


@user_router.post("/confirmation")
async def verify_register_pin(req: VerifyRegisterPin):
    return await user_controller.confirm_user(req.id, req.pin)


@user_router.post(
    "/{id}/pin",
)
async def refresh_register_pin(id: str):
    return await user_controller.refresh_register_pin(id)


@user_router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    response_model_exclude_unset=True,
)
async def get_user_by_id(id: str, request: Request):
    return await user_controller.get_user_by_id(request, id)


@user_router.get(
    "/",
    response_model=List[UserProfilePreview],
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def get_users(
    username: Optional[str] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
):
    return await user_controller.get_users_by_username(username, offset, limit)


@user_router.post("/me/following", status_code=status.HTTP_204_NO_CONTENT)
async def follow_user(request: Request, follow_request: FollowRequest):
    return await user_controller.follow_user(request, follow_request)


@user_router.delete("/me/following", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(request: Request, follow_request: FollowRequest):
    return await user_controller.unfollow_user(request, follow_request)


@user_router.get(
    "/{id}/followers",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    response_model_exclude_unset=True,
)
async def get_followers(
    id: str,
    request: Request,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
):
    return await user_controller.get_followers(request, id, offset, limit)


@user_router.get(
    "/{id}/following",
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
    response_model_exclude_unset=True,
)
async def get_following(
    id: str,
    request: Request,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
):
    return await user_controller.get_following(request, id, offset, limit)


@user_router.get("/me/stats", response_model=UserStats)
async def get_user_stats(
    request: Request, from_date: str = Query(..., description="date format YYYY-MM-DD")
):
    return await user_controller.get_user_stats(request, from_date)
