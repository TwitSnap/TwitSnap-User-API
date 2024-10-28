from fastapi import UploadFile
from firebase_admin import storage
from config.settings import FIREBASE_STORAGE_BUCKET
import os
from config.settings import logger
from firebase_admin import credentials, initialize_app


class FirebaseService:
    def __init__(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logger.info(f"Initializing Firebase with credentials from {current_dir}")
            firebase_credentials_path = os.path.join(
                current_dir,
                "..",
                "..",
                "twitsnap-82671-firebase-adminsdk-q3c3c-7613007f9d.json",
            )
            cred = credentials.Certificate(firebase_credentials_path)
            initialize_app(cred, {"storageBucket": FIREBASE_STORAGE_BUCKET})
            self.bucket = storage.bucket()
            logger.info("Firebase initialized successfully.")
        except Exception as e:
            logger.error(f"Firebase initialization error: {e}")

    async def upload_photo(self, photo: UploadFile, id: str) -> str:
        logger.debug(f"Attempting to upload photo: {photo} for user with id: {id}")

        blob = self.bucket.blob(f"{id}_{photo.filename}")
        blob.upload_from_string(await photo.read(), content_type=photo.content_type)
        blob.make_public()
        url = blob.public_url

        logger.debug(f"photo uploaded to firebase with url: {url}")
        return url


firebase_service = FirebaseService()
