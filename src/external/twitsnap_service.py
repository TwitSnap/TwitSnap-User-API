from dtos.notification.notification import Notification
from utils.requester import requester
from config.settings import (
    AUTH_API_URI,
    AUTH_API_REGISTER_PATH,
    NOTIFICATION_API_SEND_PATH,
    NOTIFICATION_API_URI,
    logger,
    NOTIFICATION_SENDER,
)
from dtos.auth.auth_user_register import AuthUserRegister

from config.settings import SERVICE_REGISTRY_URI, SERVICE_REGISTRY_VERIFY_PATH

from config.settings import API_KEY


class TwitsnapService:
    def __init__(self):
        self.requester = requester

    async def send_user_credentials_to_auth(self, user_id: str, password: str):
        url = AUTH_API_URI + AUTH_API_REGISTER_PATH  # type: ignore
        req = AuthUserRegister(id=user_id, password=password)
        logger.debug(
            f"[AuthService] - Attempting to register at {url} with data: {req.model_dump()}"
        )
        header = {"api_key": API_KEY}
        response = await self.requester.post(url, json_body=req.model_dump(), headers=header)
        logger.debug(
            f"[AuthService] - Attempt to register user - response: {response.text}"
        )

    async def send_register_pin_to_notification(
        self, email: str, username: str, pin: str
    ):
        header = {"api_key": API_KEY}
        url: str = NOTIFICATION_API_URI + NOTIFICATION_API_SEND_PATH  # type: ignore
        req = Notification(
            type="registration",
            params={"username": username, "pin": pin},
            notifications={
                "type": "email",
                "destinations": [email],
                "sender": NOTIFICATION_SENDER,
            },
        )
        logger.debug(
            f"[NotificationService] - Attempting to send pin to {email} with data: {req.model_dump()}"
        )
        res = await self.requester.post(url, json_body=req.model_dump(), headers=header)
        logger.debug(
            f"[NotificationService] - Attempt to send pin - response: {res.text}"
        )

    async def send_new_follower_notification(self, username: str, device_token: list[str]):
        url = NOTIFICATION_API_URI + NOTIFICATION_API_SEND_PATH
        req = Notification(
            type="push",
            params={"title": "Tienes nuevo seguidor",
                    "body": f" ahora te sigue {username}"},
            notifications={"type": "push", "destinations": device_token},
        )
        logger.debug(
            f"[NotificationService] - Attempting to send new follower notification to {device_token} with data: {req.model_dump()}"
        )
        res = await self.requester.post(url, json_body=req.model_dump())
        logger.debug(
            f"[NotificationService] - Attempt to send new follower notification - response: {res.text}"
        )
    async def verify_api_key(self, api_key: str):
        url = SERVICE_REGISTRY_URI + SERVICE_REGISTRY_VERIFY_PATH + api_key
        response = await self.requester.get(url)
        logger.debug(
            f"[ServiceRegistry] - Attempt to verify api key - response: {response.text}"
        )
        return response.json()
twitsnap_service = TwitsnapService()

