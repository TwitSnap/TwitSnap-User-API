from utils.requester import requester
from config.settings import logger

from config.settings import FIREBASE_API_KEY


class GoogleService:
    def __init__(
        self,
    ):
        self.requester = requester

    async def get_user_info_from_user_id_token(self, token):
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        response = await self.requester.get(url)
        logger.debug(
            f"Attempt get user info from id_token: {token} - response: {response.text}"
        )
        return response.json()

    async def get_user_info_from_access_token(self, token):
        url = f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
        response = await self.requester.get(url)
        logger.debug(
            f"Attempt get user info from access_token: {token} - response: {response.text}"
        )
        return response.json()

    async def get_user_from_firebase_token(self, token):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
        response = await self.requester.post(url, json_body={"idToken": token})
        logger.debug(
            f"Attempt get user info from firebase token: - response: {response.text}"
        )
        return response.json()


google_service = GoogleService()
