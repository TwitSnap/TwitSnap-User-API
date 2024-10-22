from contextlib import asynccontextmanager
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
    app = FastAPI(lifespan=lifespan)
    configure_middleware(app)
    configure_routes(app)
        
    @app.exception_handler(RequestValidationError)
    def _(request: Request, exc: Exception):
        return ExceptionHandler.handle_exception(exc, request)
    return app

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db.close_connection()

def configure_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    @app.middleware("http")
    async def log_request_middleware(request: Request, call_next):
        method = request.method
        url = request.url
        header = dict(request.headers)
        logger.info(f"Request url: {url} | Method: {method} | Header: {header}")
        response = await call_next(request)
        return response

def configure_routes(app: FastAPI):
    app.include_router(router)

if __name__ == "__main__":
    init_database()
    init_firebase()
    app = create_app()
    uvicorn.run(app, host = HOST, port = PORT, log_level= LOG_LEVEL)

