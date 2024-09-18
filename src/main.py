from fastapi import FastAPI

from config.db import connect_to_database

connect_to_database()
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
