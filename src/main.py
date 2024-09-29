from fastapi import FastAPI,Request
from config.settings import connect_to_database
from routes.routes import router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
def create_app():
    app = FastAPI()
    configure_middleware(app)
    configure_routes(app)
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
    connect_to_database()
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8006, log_level='debug')

