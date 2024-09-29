from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Depends
from exceptions.exception_handler import NoAuthException
from config.settings import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= AUTH_API_URI + AUTH_API_LOGIN_PATH)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        user_id: str = payload.get("userId") 
        if user_id is None:
            raise NoAuthException("Could not validate credentials")
    except JWTError:
        raise NoAuthException("Could not validate credentials")
    return user_id
