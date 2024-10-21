import random
import string
from fastapi import UploadFile
from firebase_admin import storage
from DTOs.notification.register_pin import RegisterPin
from DTOs.register.generated_pin_response import GeneratedPinResponse
from DTOs.register.google_register import GoogleRegister
from DTOs.user.edit_user import EditUser
from DTOs.user.user_profile import UserProfile
from exceptions.conflict_exception import ConflictException
from models.user import User
from repositories.user_repository import user_repository
from DTOs.register.user_register import UserRegister
from exceptions.resource_not_found_exception import ResourceNotFoundException
from config.settings import *
from utils.requester import Requester
class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def create_user(self, register_request: UserRegister):
        new_user = User(**register_request.model_dump())
        return self.user_repository.create_user(new_user)
    
    async def create_user_with_federated_identity(self, google_register: GoogleRegister):
        new_user = User(**google_register.model_dump())
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
            url = await upload_photo_to_firebase(photo, id)
            logger.debug(f"photo uploaded to firebase with link: {url}")
            user.photo = url
        return self.user_repository.update_user(user)
        
    async def get_users_by_username(self, username: str, offset: int, limit: int):
        users = self.user_repository.get_users_by_username(username, offset, limit)
        res = [UserProfile(uid = user.uid, username = user.username , photo= user.photo)for user in users]
        logger.debug(f"Found {len(users)} users with username {username}, list: {res}")
        return res
    
    async def generate_register_pin(self, user_id):
        user = await self.get_user_by_id(user_id)
    
        if user.verified:
            logger.debug(f"User with id: {user_id} is already verified")
            raise ConflictException(detail=f"User with id: {user_id} is already verified")
        
        pin = generate_pin()
        redis_conn.setex(f"{user.uid}", REGISTER_PIN_TTL, pin)
        register_pin = RegisterPin(type='registration',
                                   params={'username': user.username,
                                            'pin': pin},
                                    notifications = {"type": "email", 
                                                     "destinations": [user.email],
                                                     "sender": NOTIFICATION_SENDER}
                                                     )
        await Requester.post(NOTIFICATION_API_URI + NOTIFICATION_API_SEND_PATH, json_body = register_pin.model_dump())
        logger.debug(f"Pin generated for user with id: {user_id} - {pin}")
        return GeneratedPinResponse(pin_ttl = REGISTER_PIN_TTL)
    
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
    
def generate_pin():
    return ''.join(random.choices(string.digits, k=REGISTER_PIN_LENGHT))

async def upload_photo_to_firebase(photo: UploadFile, id: str):
    bucket = storage.bucket()
    blob = bucket.blob(f"{id}_{photo.filename}")
    blob.upload_from_string( await photo.read(), content_type = photo.content_type)
    blob.make_public()
    return blob.public_url

user_service = UserService(user_repository)
