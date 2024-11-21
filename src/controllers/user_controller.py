from datetime import datetime
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from dtos.register.user_register import UserRegister
from dtos.user.edit_user import EditUser
from dtos.user.update_user_form import UpdateUserForm
from exceptions.bad_request_exception import BadRequestException
from services.user_service import user_service
from exceptions.exception_handler import ExceptionHandler
from config.settings import logger


class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    async def register(self, user_register_data: UserRegister):
        try:
            return await self.user_service.register(user_register_data)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def get_user_by(self, email: str):
        try:
            return await self.user_service.get_user_by_email(email)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    # endpoints that requires user_id from header
    async def get_user_by_id(self, request: Request, id: str):  # type: ignore
        try:
            my_uid: str | None = self.get_current_user(request)
            if id == "me" or id == my_uid:
                logger.debug(f"Getting my user with id: {my_uid}")
                return await self.user_service.get_my_user(my_uid)
            logger.debug(f"Getting user with id: {id}")
            return await self.user_service.get_user_by_id(id, my_uid)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def edit_user_by_id(self, request: Request, update_form: UpdateUserForm):
        try:
            my_uid: str | None = self.get_current_user(request)
            new_user_data = EditUser(
                username=update_form.username,
                phone=update_form.phone,
                country=update_form.country,
                description=update_form.description,
                interests=update_form.interests,
            )
            if update_form.photo and not update_form.photo.filename.endswith(
                (".jpg", ".jpeg", ".png")
            ):
                logger.debug(
                    f"Received file with content type {update_form.photo.content_type} - Only images are supported"
                )
                raise RequestValidationError(
                    f"Received file with content type {update_form.photo.content_type} - Only images are supported"
                )
            return await self.user_service.edit_user_by_id(
                new_user_data, update_form.photo, my_uid
            )
        except Exception as e:
            return ExceptionHandler.handle_exception(e, request)

    async def get_users_by_username(self, username: str, offset: int, limit: int):
        try:
            return await self.user_service.get_users_by_username(
                username, offset, limit
            )
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def refresh_register_pin(self, user_id: str):
        try:
            return await self.user_service.generate_register_pin(user_id)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def confirm_user(self, user_id: str, pin: str):
        try:
            return await self.user_service.confirm_user(user_id, pin)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def ban_or_unban_user(self, user_id: str):
        try:
            return await self.user_service.ban_or_unban_user(user_id)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def get_user_by_id_admin(self, user_id: str):
        try:
            return await self.user_service.get_user_by_id_admin(user_id)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def get_all_users(self, offset: int, limit: int):
        try:
            return await self.user_service.get_all_users(offset, limit)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def follow_user(self, request: Request, follow_request):
        try:
            my_uid: str | None = self.get_current_user(request)
            return await self.user_service.follow_user(my_uid, follow_request.id)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def unfollow_user(self, request: Request, follow_request):
        try:
            my_uid: str | None = self.get_current_user(request)
            return await self.user_service.unfollow_user(my_uid, follow_request.id)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def get_followers(self, request: Request, id: str, offset: int, limit: int):
        try:
            my_uid: str | None = self.get_current_user(request)
            if id == "me" or id == my_uid:
                logger.debug(f"Getting my followers with id: {my_uid}")
                return await self.user_service.get_my_followers(my_uid, offset, limit)

            return await self.user_service.get_followers(my_uid, id, offset, limit)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def get_following(self, request: Request, id: str, offset: int, limit: int):
        try:
            my_uid: str | None = self.get_current_user(request)
            if id == "me" or id == my_uid:
                logger.debug(f"Getting my following with id: {my_uid}")
                return await self.user_service.get_my_following(my_uid, offset, limit)
            logger.debug(f"Getting following of user with id: {id}, my id: {my_uid}")
            return await self.user_service.get_following(my_uid, id, offset, limit)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def get_user_stats(self, req: Request, from_date: str):
        try:
            uid = self.get_current_user(req)
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
            return await self.user_service.get_user_stats(uid, from_date)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    async def get_user_metrics(self, metric_type: str):
        try:
            logger.debug(f"Getting metrics for type: {metric_type}")
            if metric_type not in [
                "registration",
                "banned",
                "country_distribution",
                None,
            ]:
                raise BadRequestException(
                    detail="Invalid metric type, valid values are: registration, banned, country_distribution"
                )
            return await self.user_service.get_metrics(metric_type)
        except Exception as e:
            return ExceptionHandler.handle_exception(e)

    def get_current_user(self, req: Request):
        user_id = req.headers.get("user_id")
        logger.debug(f"User id found in headers: {user_id}")
        if user_id is None:
            raise BadRequestException(detail="User id not found in headers")
        return user_id


user_controller = UserController(user_service)
