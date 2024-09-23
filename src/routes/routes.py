from fastapi import APIRouter
from routes.register_routes import register_router
from routes.user_routes import user_router

router = APIRouter()

router.include_router(register_router, prefix='/v1/register')
router.include_router(user_router, prefix = '/v1/users')
