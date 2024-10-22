from DTOs.notification.register_pin import RegisterPin
from utils.requester import requester
from config.settings import *
from DTOs.auth.auth_user_register import AuthUserRegister

class TwitsnapService:
    def __init__(self):
        self.requester = requester
    
    async def send_user_credentials_to_auth(self,user_id: str, password: str):
        url = AUTH_API_URI + AUTH_API_REGISTER_PATH # type: ignore
        req = AuthUserRegister(id = user_id, password = password)
        logger.debug(f"[AuthService] - Attempting to register at {url} with data: {req.model_dump()}")
        response = await self.requester.post(url, json_body = req.model_dump())
        logger.debug(f"[AuthService] - Attempt to register user - response: {response.text}")
    
    async def send_register_pin_to_notification(self, email: str, username: str, pin: str):
        url: str = NOTIFICATION_API_URI + NOTIFICATION_API_SEND_PATH # type: ignore
        req = RegisterPin(type='registration',params={'username': username,'pin': pin},
                                    notifications = {"type": "email", 
                                                        "destinations": [email],
                                                        "sender": NOTIFICATION_SENDER}
                                                        )
        logger.debug(f"[NotificationService] - Attempting to send pin to {email} with data: {req.model_dump()}")
        await self.requester.post(url, json_body = req.model_dump())

twitsnap_service = TwitsnapService()