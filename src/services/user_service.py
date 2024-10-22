import random
import string
from fastapi import UploadFile
from DTOs.auth.aurh_user_response import AuthUserResponse
from DTOs.backoffice.ban_user_request import BanUserRequest
from DTOs.notification.register_pin import RegisterPin
from DTOs.register.generated_pin_response import GeneratedPinResponse
from DTOs.register.google_register import GoogleRegister
from DTOs.user.edit_user import EditUser
from DTOs.user.user_profile import UserProfile
from DTOs.user.user_profile_preview import UserProfilePreview
from exceptions.conflict_exception import ConflictException
from models.user import User
from repositories.user_repository import user_repository
from DTOs.register.user_register import UserRegister
from exceptions.resource_not_found_exception import ResourceNotFoundException
from config.settings import *
from external.firebase_service import firebase_service
from external.twitsnap_service import twitsnap_service

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.firebase_service = firebase_service
        self.twitsnap_service = twitsnap_service

    async def create_user(self, register_request: UserRegister):
        new_user = User(**register_request.model_dump())
        return self.user_repository.save(new_user)
    
    async def create_user_with_federated_identity(self, google_register: GoogleRegister):
        new_user = User(**google_register.model_dump())
        new_user.verified = True
        return self.user_repository.save(new_user)
    
    async def get_user_by_email(self, email):
        logger.debug(f"Attempting to get user id by email: {email}")
        user = self.user_repository.find_user_by_email(email)
        if user is None:
            logger.debug(f"User not found with email: {email}")
            raise ResourceNotFoundException(detail=f"User not found with email: {email}")
        logger.debug(f"Found user with email: {email} and id: {user.uid}")
        logger.debug(f"user is_banned status: {user.is_banned}")
        return AuthUserResponse(uid = user.uid, is_banned = user.is_banned)
    

    async def get_user_by_id(self, id, my_uid = None):
        user = await self._get_user_by_id(id)
        if user.is_banned:
            logger.debug(f"User with id: {id} is banned")
            raise ResourceNotFoundException(detail=f"User with id: {id} not found")
        
        if my_uid:
            my_user = await self._get_user_by_id(my_uid)
        
        return UserProfile(uid = user.uid, 
                           username = user.username, 
                           phone = user.phone,
                           country = user.country, 
                           description = user.description,
                           photo = user.photo,
                           amount_of_followers = len(user.followers),
                           amount_of_following = len(user.following),
                           is_follwed_by_me = user.followers.is_connected(my_user) if my_uid else None,
                           )
    
    async def get_my_user(self, user_id):
        user = await self._get_user_by_id(user_id)
        return UserProfile(uid = user.uid, 
                           username = user.username, 
                           phone = user.phone,
                           country = user.country, 
                           description = user.description, 
                           photo = user.photo,
                           email = user.email,
                           verified = user.verified,
                           amount_of_followers = len(user.followers),
                           amount_of_following = len(user.following),
                           )

    async def _get_user_by_id(self, id):
        user = self.user_repository.find_user_by_id(id)
        if user is None:
            logger.debug(f"User not found with id: {id}")
            raise ResourceNotFoundException(detail=f"User not found with id: {id}")
        return user

    async def exists_user_by_email(self, email):
        return self.user_repository.find_user_by_email(email) is not None
    
    async def edit_user_by_id(self, user_data: EditUser, photo: UploadFile , id :str):
        logger.debug(f"Attempting to change user data with id: {id}. New values: {user_data}")
        user = await self._get_user_by_id(id)

        for attr, value in user_data.model_dump().items():
            if value is not None:
                setattr(user, attr, value)

        if photo:
            url = await self.firebase_service.upload_photo(photo, id)
            user.photo = url
        eddited_user = self.user_repository.save(user)
        return UserProfile(uid = eddited_user.uid,
                            username = eddited_user.username,
                            phone = eddited_user.phone,
                            country = eddited_user.country,
                            email= eddited_user.email,
                            description = eddited_user.description,
                            photo = eddited_user.photo,
                            amount_of_followers = len(eddited_user.followers),
                            amount_of_following = len(eddited_user.following)
                            )
        
    async def get_users_by_username(self, username: str, offset: int, limit: int):
        users = self.user_repository.get_users_by_username(username, offset, limit)
        res = [UserProfilePreview(uid = user.uid, username = user.username , photo= user.photo )for user in users]
        logger.debug(f"Found {len(users)} users with username {username}, list: {res}")
        return res
    
    async def confirm_user(self, user_id, pin):
        user = await self._get_user_by_id(user_id)

        if user.verified:
            logger.debug(f"User with id: {user_id} is already verified")
            raise ConflictException(detail=f"User with id: {user_id} is already verified")
        
        pin_from_uid = redis_conn.get(user_id)

        if pin_from_uid is None:
            logger.debug(f"Pin {pin} is invalid or expired")
            raise ResourceNotFoundException(detail=f"Pin {pin} is invalid or expired")
            
        if pin_from_uid.decode() != pin:
            logger.debug(f"Pin {pin} is invalid for user with id: {user_id}")
            raise ResourceNotFoundException(detail=f"Pin {pin} is invalid")
        
        user.verified = True
        self.user_repository.save(user)

        return user
    async def ban_user(self, user_id, req: BanUserRequest):
        user = await self._get_user_by_id(user_id)    
        user.is_banned = req.is_banned
        self.user_repository.save(user)
        return 
    
    async def get_user_by_id_admin(self, user_id):
       return await self._get_user_by_id(user_id)
    
    async def get_all_users(self, offset: int, limit: int):
        return self.user_repository.get_all_users(offset, limit)
    
    async def generate_register_pin(self, user_id):
        user = await self._get_user_by_id(user_id)

        if user.verified:
            logger.debug(f"User with id: {user_id} is already verified")
            raise ConflictException(detail=f"User with id: {user_id} is already verified")
        
        pin = self._generate_pin()
        redis_conn.setex(f"{user.uid}", REGISTER_PIN_TTL, pin)
        await self.twitsnap_service.send_register_pin_to_notification(user.email ,user.uid, pin)
        logger.debug(f"Pin generated for user with id: {user_id} - {pin}")
        return GeneratedPinResponse(pin_ttl = REGISTER_PIN_TTL)
    
    def _generate_pin(self):
        return ''.join(random.choices(string.digits, k=REGISTER_PIN_LENGHT))

user_service = UserService(user_repository)
