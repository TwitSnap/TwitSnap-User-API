from DTOs.register.google_register import GoogleRegister
from config.settings import logger
from exceptions.user_registration_exception import UserRegistrationException
from services.user_service import user_service
from external.twitsnap_service import twitsnap_service
from external.google_service import google_service
from DTOs.register.user_register import UserRegister
from exceptions.conflict_exception import ConflictException
from fastapi import status
from starlette.responses import JSONResponse

from src.DTOs.user.user_builder import UserBuilder


class RegisterService:
    def __init__(self):
        self.service = user_service
        self.twitsnap_service = twitsnap_service
        self.google_service = google_service

    async def register(self, register_data: UserRegister):

        if await self.service.exists_user_by_email(register_data.email):
            logger.debug(
                f"The email address {register_data.email} is already registered."
            )
            raise ConflictException(
                f"The email address {register_data.email} is already registered."
            )
        try:
            logger.debug(f"Attempting to register user with data: {register_data}")
            user = await self.service.create_user(register_data.model_dump())
            await self.twitsnap_service.send_user_credentials_to_auth(
                user.uid, register_data.password
            )
            await self.service.generate_register_pin(user.uid)

        except Exception as e:
            self.service.delete_user_by_id(user.uid)
            logger.error(f"Error attempt to register user: {str(e)}")
            raise UserRegistrationException(str(e))
        return user

    async def register_with_google(self, token: GoogleRegister):
        user_info = await self.google_service.get_user_from_firebase_token(token.token)
        logger.debug(f"User info from firebse token: {user_info}")
        provider_info = user_info["users"][0]["providerUserInfo"][0]
        id = provider_info["rawId"]
        email = provider_info["email"]
        name = provider_info["displayName"]
        photo = provider_info["photoUrl"]
        google_register = {
            "uid": id,
            "username": name,
            "photo": photo,
            "email": email,
            "provider": "google",
            "verified": True,
        }
        logger.debug(f"attempting to find user with id: {id}")
        user = self.service.user_repository.find_user_by_id(id)
        logger.debug(f"user: {user}")
        if user is not None:
            logger.debug(
                f"User already registered with email: {user.email}, id: {user.uid} , username: {user.username}"
            )
            res = UserBuilder(user).with_uid().with_is_banned().build()
            return JSONResponse(status_code=status.HTTP_200_OK, content=res)
        logger.debug(
            f"Attempting to register with google id: {id}, email: {email}, name: {name}, photo: {photo}"
        )
        user = await self.service.create_user(google_register)
        res = UserBuilder(user).with_uid().with_is_banned().build()

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=res)


register_service = RegisterService()
