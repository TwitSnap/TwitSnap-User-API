from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from exceptions.bad_request_exception import BadRequestException
from exceptions.conflict_exception import ConflictException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from config.settings import logger

from exceptions.no_auth_exception import UnauthorizedException


class ExceptionHandler:
    @staticmethod
    def handle_exception(exc: Exception, request: Request = None) -> JSONResponse:

        if isinstance(exc, ResourceNotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"message": exc.detail}
            )
        elif isinstance(exc, ConflictException):
            logger.debug(f"Conflict error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT, content={"message": exc.detail}
            )
        elif isinstance(exc, RequestValidationError):
            logger.debug(f"Validation error : {exc.errors()}")
            message = exc.errors()[0]["msg"]
            message = message.replace("Value error, ", "").strip()
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": str(message)},
            )
        elif isinstance(exc, UnauthorizedException):
            logger.debug(f"Unauthorized error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content={"message": exc.detail}
            )
        elif isinstance(exc, ValidationError):
            logger.debug(f"Validation error: {exc.errors()}")
            message = exc.errors()[0]["msg"]
            message = message.replace("Value error, ", "").strip()
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": str(message)},
            )
        elif isinstance(exc, BadRequestException):
            logger.debug(f"Bad request: {exc}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.detail}
            )
        else:
            logger.error(f"Internal server error: {exc}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "Internal server error"},
            )
