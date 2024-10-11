from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from exceptions.no_auth_exception import NoAuthException
from exceptions.conflict_exception import ConflictException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from models.user import User
from config.settings import logger

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
            logger.debug(f"Received data: {exc.body}")
            return JSONResponse(
                status_code=422,
                content={"detail": exc.errors()},
            )
        else:
            logger.error(f"Internal server error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error: {exc}"}
            )