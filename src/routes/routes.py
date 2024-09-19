from fastapi import APIRouter
from routes.session_routes import session_router

router = APIRouter()

router.include_router(session_router)
