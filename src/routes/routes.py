from fastapi import APIRouter
from routes.register_routes import register_router
from routes.user_routes import user_router

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(register_router, prefix = '/register')
router.include_router(user_router, prefix = '/users')
