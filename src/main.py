from fastapi import FastAPI,Request
from fastapi.exceptions import RequestValidationError
from config.settings import *
from exceptions.exception_handler import ExceptionHandler
from routes.routes import router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.settings import *
def create_app():
    app = FastAPI()
    configure_middleware(app)
    configure_routes(app)  
    @app.exception_handler(RequestValidationError)
    async def _(request: Request, exc: Exception):
        return await ExceptionHandler.handle_exception(exc, request)
    return app

def configure_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key='',
    )

def configure_routes(app: FastAPI):
    app.include_router(router)

if __name__ == "__main__":
    init_database()
    init_firebase()
    app = create_app()
    uvicorn.run(app, host = HOST, port = PORT, log_level= LOG_LEVEL)

