from fastapi import FastAPI,Request
from config.settings import db
from routes.routes import router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from exceptions.exeption_handler import ExceptionHandler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(
    SessionMiddleware,
    secret_key='SECRET_KEY',
)
app.include_router(router)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return await ExceptionHandler.handle_exception(request, exc)

# TODO:
# - conectar con microservicio de auth
# - validaciones
# - tests
