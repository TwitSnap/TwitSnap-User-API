from fastapi import FastAPI
from config.settings import db
from routes.routes import router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware


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

# TODO:
# - conectar con microservicio de auth
# - validaciones
# - tests
