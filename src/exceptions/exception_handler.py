from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError
from pydantic import ValidationError
from exceptions.bad_request_exception import BadRequestException
from exceptions.no_auth_exception import NoAuthException
from exceptions.conflict_exception import ConflictException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from models.user import User
from config.settings import logger
from fastapi import HTTPException

class ExceptionHandler:
    @staticmethod
    async def handle_exception(exc: Exception, request: Request = None):

        if isinstance(exc, ResourceNotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": exc.detail}
            )
        elif isinstance(exc, ConflictException):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": exc.detail}
            )
        elif isinstance(exc, NoAuthException):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": exc.detail}
            )
        elif isinstance(exc, RequestValidationError):
            logger.debug(f"Validation error at {request.url}: {exc.errors()}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": str(exc)},
            )
        elif isinstance(exc, ValidationError):
            logger.debug(f"Validation error: {exc.errors()}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": exc.errors()},
            )
        elif isinstance(exc, ExpiredSignatureError):
            logger.debug(f"Token expired: {exc}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        elif isinstance(exc, BadRequestException):
            logger.debug(f"Bad request: {exc}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": exc.detail}
            )
        else:
            logger.error(f"Internal server error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error"}
            )