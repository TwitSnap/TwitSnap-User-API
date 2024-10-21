from fastapi import Request
from config.settings import logger
from exceptions.bad_request_exception import BadRequestException
from exceptions.exception_handler import ExceptionHandler

def get_current_user(req: Request):
    try:
        user_id = req.headers.get("user_id")
        logger.debug(f"User id found in headers: {user_id}")
        if user_id is None:
            raise BadRequestException(detail= "User id not found in headers")
        return user_id
    except BadRequestException as e:
        logger.error(f"Error while trying to get current user: {str(e)}")
        ExceptionHandler.handle_exception(e)

