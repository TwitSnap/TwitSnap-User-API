from fastapi import FastAPI
from config.db import connect_to_database
from controllers.register_controller import register_router

connect_to_database()
app = FastAPI()
app.include_router(register_router)
