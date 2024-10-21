from fastapi.responses import JSONResponse
from DTOs.register.google_register import GoogleRegister
from config.settings import *
from exceptions.user_registration_exception import UserRegistrationException
from services.user_service import user_service
from DTOs.register.user_register import UserRegister
from DTOs.auth.auth_user_register import AuthUserRegister
from fastapi import requests, status
from exceptions.conflict_exception import ConflictException

from utils.requester import Requester
class RegisterService:
    def __init__(self):
        self.service = user_service

    async def register(self, register_data: UserRegister):

        if await self.service.exists_user_by_email(register_data.email):
            logger.debug(f"The email address {register_data.email} is already registered.")
            raise ConflictException(f"The email address {register_data.email} is already registered.")
        try:
            logger.debug(f"Attempting to register user with data: {register_data}")
            user = await self.service.create_user(register_data)
            auth_user_register = AuthUserRegister(id = user.uid, password = register_data.password)

            url = AUTH_API_URI + AUTH_API_REGISTER_PATH
            logger.debug(f"[AuthService] - Attempting to register at {url} with data: {auth_user_register.model_dump()}")
            response = await Requester.post(url, json_body = auth_user_register.model_dump())
            logger.debug(f"[AuthService] - Attempt to register user with data: {auth_user_register.model_dump()} - response: {response.text}")
            await self.service.generate_register_pin(user.uid)
        except Exception as e:
            user.delete()
            logger.error(f"Error attempt to register user: {str(e)}")
            raise UserRegistrationException(str(e))
        return user    
        
    
    async def register_with_google(self, token : GoogleRegister):
        user_info = await verify_google_token(token.token)
        id = user_info['sub'] 
        email = user_info['email']     
        name = user_info['name'] 
        photo = user_info['picture']
        google_register = GoogleRegister(uid = id, email = email, username = name, photo = photo)        

        user = self.service.user_repository.find_user_by_email(email)
        if user is None:
            logger.debug(f"Attempting to Google-register with data: id: {id}, email: {email}, name: {name}, photo: {photo}")   
            user = await self.service.create_user_with_federated_identity(google_register)
            # return await self.service.generate_register_pin(user.uid)
            return user
        logger.debug(f"User already registered with email: {email}, id: {id} , username: {name}")

        return user
    
async def verify_google_token(token):
    # con access token
    # url = "https://www.googleapis.com/oauth2/v1/userinfo"
    # headers = {
    #     "Authorization": f"Bearer {token}"
    # }

    url = f'https://oauth2.googleapis.com/tokeninfo?id_token={token}'

    response = await Requester.get(url)
    logger.debug(f"Attemptt to verify google token: {token} - response: {response.text}")
    return response.json()
    
register_service = RegisterService()