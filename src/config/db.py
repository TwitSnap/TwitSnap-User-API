# db/database.py
import os
from dotenv import load_dotenv
from neomodel import config, db

load_dotenv()

def get_database_url():
    protocol = os.getenv("NEO4J_PROTOCOL")
    url = os.getenv("NEO4J_HOST_PORT")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    return f"{protocol}://{username}:{password}@{url}"

def connect_to_database():
    config.DATABASE_URL = get_database_url()
    try:
        db.cypher_query("MATCH (n) RETURN n LIMIT 1")
        print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print("Error de conexión:", e)

