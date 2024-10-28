from fastapi import APIRouter, status
from models.interest import Interest

resource_router = APIRouter()


@resource_router.get("/", status_code=status.HTTP_200_OK)
async def get_available_interests():
    return {"interests": [i.name for i in Interest.nodes.all()]}
