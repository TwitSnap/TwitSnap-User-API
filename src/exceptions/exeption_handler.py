from fastapi import Request, status
from fastapi.responses import JSONResponse
from exceptions.conflict_exception import ConflictException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from models.user import User

class ExceptionHandler:
    @staticmethod
    async def handle_exception(req: Request, exc: Exception):

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
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error: {exc}"}
            )