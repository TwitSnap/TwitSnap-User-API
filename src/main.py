from fastapi import FastAPI
from config.db import connect_to_database
from routes.routes import router

connect_to_database()
app = FastAPI()
app.include_router(router)
