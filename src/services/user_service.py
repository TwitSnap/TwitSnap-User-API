from fastapi import UploadFile
from firebase_admin import storage
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
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, register_request: UserRegister):
        new_user = User(**register_request.model_dump())
        return self.user_repository.create_user(new_user)
    
    async def create_user_with_federated_identity(self, google_register: GoogleRegister):
        new_user = User(**google_register.model_dump())
        new_user.verified = True
        return self.user_repository.create_user(new_user)
    
    async def get_user_id_by_email(self, email):
        logger.debug(f"Attempting to get user id by email: {email}")
        user = self.user_repository.find_user_by_email(email)
        if user is None:
            logger.debug(f"User not found with email: {email}")
            raise ResourceNotFoundException(detail=f"User not found with email: {email}")
        logger.debug(f"Found user with email: {email} and id: {user.uid}")
        return user.uid
    
    async def get_user_by_id(self, id, my_uid = None):
        user = await self._get_user_by_id(id)
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
                           is_follwed_by_me = user.followers.is_connecected(my_user) if my_uid else None,
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
            logger.debug(f"Attempting to upload photo: {photo} for user with id: {id}")
            url = await upload_photo_to_firebase(photo, id)
            logger.debug(f"photo uploaded to firebase with link: {url}")
            user.photo = url
        eddited_user = self.user_repository.update_user(user)
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
        user = await self.get_user_by_id(user_id)

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
        self.user_repository.update_user(user)

        return user
    
async def upload_photo_to_firebase(photo: UploadFile, id: str):
    bucket = storage.bucket()
    blob = bucket.blob(f"{id}_{photo.filename}")
    blob.upload_from_string( await photo.read(), content_type = photo.content_type)
    blob.make_public()
    return blob.public_url

user_service = UserService(user_repository)
