from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from fastapi import Depends
from exceptions.exception_handler import NoAuthException
from config.settings import *

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY)
        user_id: str = payload.get("userId") 
        logger.debug(f"User ID from token: {user_id}")
        if user_id is None:
            raise NoAuthException(f"Could not validate credentials")
    except JWTError as e:
        logger.warning(f"error decoding token: {token} - {e}")
        raise NoAuthException("Could not validate credentials")
    return user_id
