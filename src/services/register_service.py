import random
import string
from fastapi.responses import JSONResponse
from DTOs.notification.register_pin import RegisterPin
from DTOs.register.generated_pin_response import GeneratedPinResponse
from DTOs.register.google_register import GoogleRegister
from config.settings import *
from exceptions.user_registration_exception import UserRegistrationException
from services.user_service import user_service
from external.twitsnap_service import twitsnap_service
from external.google_service import google_service
from DTOs.register.user_register import UserRegister
from DTOs.auth.auth_user_register import AuthUserRegister
from exceptions.conflict_exception import ConflictException

from utils.requester import Requester
class RegisterService:
    def __init__(self):
        self.service = user_service
        self.twitsnap_service = twitsnap_service
        self.google_service  = google_service

    async def register(self, register_data: UserRegister):

        if await self.service.exists_user_by_email(register_data.email):
            logger.debug(f"The email address {register_data.email} is already registered.")
            raise ConflictException(f"The email address {register_data.email} is already registered.")
        try:
            logger.debug(f"Attempting to register user with data: {register_data}")
            user = await self.service.create_user(register_data)
            # await self.twitsnap_service.send_user_credentials_to_auth(user.uid, register_data.password)
            # await self.service.generate_register_pin(user.uid)

        except Exception as e:
            user.delete()
            logger.error(f"Error attempt to register user: {str(e)}")
            raise UserRegistrationException(str(e))
        return user    
        
    async def register_with_google(self, token : GoogleRegister):
        user_info = await self.google_service.get_user_info_from_user_id_token(token.token)
        id = user_info['sub'] 
        email = user_info['email']     
        name = user_info['name'] 
        photo = user_info['picture']
        google_register = GoogleRegister(uid = id, email = email, username = name, photo = photo)        

        user = self.service.user_repository.find_user_by_email(email)
        if user is None:
            logger.debug(f"Attempting to register with google: id: {id}, email: {email}, name: {name}, photo: {photo}")   
            user = await self.service.create_user_with_federated_identity(google_register)
            return user
        logger.debug(f"User already registered with email: {email}, id: {id} , username: {name}")
        return user
    
register_service = RegisterService()