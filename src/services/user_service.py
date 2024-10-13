from fastapi import UploadFile
from firebase_admin import storage
from DTOs.user.edit_user import EditUser
from DTOs.user.user_profile import UserProfile
from models.user import User
from repositories.user_repository import user_repository
from DTOs.register.user_register import UserRegister
from exceptions.resource_not_found_exception import ResourceNotFoundException
from config.settings import logger
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, register_request: UserRegister):
        new_user = User(**register_request.model_dump())
        return self.user_repository.create_user(new_user)
    
    async def create_user_with_federated_identity(self, id, email, username):
        new_user = User(username = username,
                        email = email,
                        uid = id,)
        return self.user_repository.create_user(new_user)
    
    async def get_user_id_by_email(self, email):
        logger.debug(f"Attempting to get user id by email: {email}")
        user = self.user_repository.find_user_by_email(email)
        if user is None:
            logger.debug(f"User not found with email: {email}")
            raise ResourceNotFoundException(detail=f"User not found with email: {email}")
        return user.uid
    
    async def get_user_by_id(self, id):
        user = self.user_repository.find_user_by_id(id)
        if user is None:
            logger.debug(f"User not found with id: {id}")
            raise ResourceNotFoundException(detail=f"User not found with id: {id}")
        return user
    
    async def exists_user_by_email(self, email):
        return self.user_repository.find_user_by_email(email) is not None
    
    async def edit_user_by_id(self, user_data: EditUser, photo: UploadFile , id :str):
        logger.debug(f"Attempting to change user data with id: {id}. New values: {user_data}")
        user = await self.get_user_by_id(id)
        if user_data.username is not None:
            user.username = user_data.username
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.country is not None:
            user.country = user_data.country
        if user_data.description is not None:
            user.description = user_data.description
        if photo is not None:
            bucket = storage.bucket()
            blob = bucket.blob(f"{id}_{photo.filename}")
            blob.upload_from_string( await photo.read(), content_type = photo.content_type)
            blob.make_public()
            url = blob.public_url
            logger.debug(f"photo uploaded to {url}")
            user.photo = url
        return self.user_repository.update_user(user)
        
    async def get_all_users(self):
        users = self.user_repository.get_all_users()
        return [UserProfile(uid = user.uid, username = user.username )for user in users]
    
    async def delete_all_users(self):
        return self.user_repository.delete_all_users()
    
    async def get_users_by_username(self, username: str, offset: int, limit: int):
        users = self.user_repository.get_users_by_username(username, offset, limit)
        res = [UserProfile(uid = user.uid, username = user.username )for user in users]
        logger.debug(f"Found {len(users)} users with username {username}, list: {res}")
        return res
user_service = UserService(user_repository)