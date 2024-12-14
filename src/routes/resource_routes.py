from fastapi import APIRouter, status, Request
from models.interest import Interest
from config.settings import logger
from external.twitsnap_service import twitsnap_service
from exceptions.exception_handler import ExceptionHandler

resource_router = APIRouter()


@resource_router.get("/", status_code=status.HTTP_200_OK)
async def get_available_interests(request: Request):
    try:
        api_key = get_api_key_from_header(request)
        if api_key is not None:
            res = await twitsnap_service.verify_api_key(api_key)
        return {"interests": [i.name for i in Interest.nodes.all()]}
    except Exception as e:
        return ExceptionHandler.handle_exception(e)

def get_api_key_from_header(req: Request):
    api_key = req.headers.get("api_key")
    logger.debug(f"Api key found in headers: {api_key}")
    if api_key is None:
       logger.error("Api key not found in headers")
       return None
    return api_key