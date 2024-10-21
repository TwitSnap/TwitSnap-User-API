from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from fastapi import Depends
from exceptions.exception_handler import ExceptionHandler, NoAuthException
from config.settings import *

bearer_scheme = HTTPBearer()
# se reemplaza por user_id en el header
# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
#     try:
#         token = credentials.credentials
#         payload = jwt.decode(token, SECRET_KEY)
#         user_id: str = payload.get("userId") 
#         logger.debug(f"User ID from token: {user_id}")
#         if user_id is None:
#             raise NoAuthException(f"Could not validate user_id : {user_id} from token: {token}")
#     except Exception as e:
#         logger.warning(f"error decoding token: {token} - {e}")
#         return await ExceptionHandler.handle_exception(e)
    

    # return user_id
