import os
from neomodel import config, db
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
DB_PROTOCOL = os.getenv("NEO4J_PROTOCOL")
DB_URI = os.getenv("NEO4J_HOST_PORT")
DB_USERNAME = os.getenv("NEO4J_USERNAME")
DB_PASSWORD = os.getenv("NEO4J_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
AUTH_API_URI = os.getenv("AUTH_API_URI")
AUTH_API_REGISTER_PATH = os.getenv("AUTH_API_REGISTER_PATH")
AUTH_API_LOGIN_PATH = os.getenv("AUTH_API_LOGIN_PATH")
DB_TEST_URL = 'bolt://neo4j:testpassword@localhost:7687'

def connect_to_database():
    try:
        config.DATABASE_URL = f"{DB_PROTOCOL}://{DB_USERNAME}:{DB_PASSWORD}@{DB_URI}"
        db.set_connection(config.DATABASE_URL)
        print(f"Connecting to database at {config.DATABASE_URL}")
        db.cypher_query("MATCH (n) DETACH DELETE n")
        print("Successfully connected to the database.")
        
    except Exception as e:
        print("Database connection error:", e)
        